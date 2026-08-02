"""
Background remover with realistic contact + ambient shadow compositing.

Pipeline:
  1. Extract subject + alpha mask (rembg)
  2. Build a squashed, blurred silhouette -> two shadow layers (contact + ambient)
  3. Composite: background -> shadow (multiply-ish blend) -> subject (alpha paste)

Usage:
    python bg_remove_shadow.py input.jpg output.png --bg-color 255,255,255
    python bg_remove_shadow.py input.jpg output.png --bg-image studio_floor.jpg
"""

import io
import argparse
import numpy as np
from PIL import Image, ImageFilter
from rembg import remove, new_session


# ---- Step 1: Extraction -----------------------------------------------

def extract_subject(input_data: bytes, model_name: str = "isnet-general-use") -> Image.Image:
    """Returns an RGBA image with background removed.
    Swap model_name to 'birefnet-general' or a RMBG-2.0 wrapper for higher quality."""
    session = new_session(model_name)
    output_bytes = remove(input_data, session=session)
    return Image.open(io.BytesIO(output_bytes)).convert("RGBA")


# ---- Step 2: Shadow generation -----------------------------------------

def _get_bottom_bound(alpha: np.ndarray) -> int:
    """Find the lowest row containing non-transparent pixels (the subject's base)."""
    rows_with_content = np.where(alpha.max(axis=1) > 10)[0]
    if len(rows_with_content) == 0:
        return alpha.shape[0] - 1
    return int(rows_with_content[-1])


def _make_shadow_layer(
    alpha_img: Image.Image,
    squash: float,
    blur_radius: int,
    opacity: float,
    y_offset: int,
    x_shear: float = 0.0,
) -> Image.Image:
    """
    Build one shadow silhouette layer.
      squash       - vertical compression (0.15 = tight contact shadow, 0.4 = ambient)
      blur_radius  - gaussian blur px (small = sharp contact, large = soft ambient)
      opacity      - 0-1 max darkness of the shadow
      y_offset     - px to nudge the shadow down from the subject's base
      x_shear      - horizontal skew to simulate an angled light source
    """
    w, h = alpha_img.size
    alpha_np = np.array(alpha_img)
    base_y = _get_bottom_bound(alpha_np)

    # Squash the silhouette vertically to fake a ground-plane projection
    squashed_h = max(1, int(h * squash))
    silhouette = alpha_img.resize((w, squashed_h), Image.LANCZOS)

    # Optional shear for angled light
    if x_shear != 0:
        silhouette = silhouette.transform(
            (w, squashed_h),
            Image.AFFINE,
            (1, x_shear, -x_shear * squashed_h / 2, 0, 1, 0),
            resample=Image.BICUBIC,
            fillcolor=0,
        )

    canvas = Image.new("L", (w, h), 0)
    paste_y = min(h - squashed_h, base_y - squashed_h + y_offset)
    canvas.paste(silhouette, (0, max(0, paste_y)))

    canvas = canvas.filter(ImageFilter.GaussianBlur(blur_radius))

    shadow_np = (np.array(canvas).astype(np.float32) / 255.0) * opacity
    return Image.fromarray((shadow_np * 255).astype(np.uint8), "L")


def build_dual_shadow(subject_rgba: Image.Image) -> Image.Image:
    """Combines a tight contact shadow + a soft ambient shadow into one grayscale layer."""
    alpha = subject_rgba.split()[-1]

    contact = _make_shadow_layer(
        alpha, squash=0.10, blur_radius=6, opacity=0.55, y_offset=2
    )
    ambient = _make_shadow_layer(
        alpha, squash=0.35, blur_radius=30, opacity=0.20, y_offset=10
    )

    combined = np.maximum(np.array(contact, dtype=np.float32), np.array(ambient, dtype=np.float32))
    return Image.fromarray(combined.astype(np.uint8), "L")


# ---- Step 3: Composite ---------------------------------------------------

def composite(subject_rgba: Image.Image, shadow_gray: Image.Image, background: Image.Image) -> Image.Image:
    bg = background.convert("RGBA").resize(subject_rgba.size)

    # Multiply-blend the shadow onto the background
    bg_np = np.array(bg).astype(np.float32)
    shadow_np = np.array(shadow_gray).astype(np.float32) / 255.0  # 0..1 darkness
    for c in range(3):
        bg_np[..., c] = bg_np[..., c] * (1.0 - shadow_np * 0.7)  # 0.7 = max shadow strength
    shadowed_bg = Image.fromarray(np.clip(bg_np, 0, 255).astype(np.uint8), "RGBA")

    # Paste subject on top using its own alpha
    shadowed_bg.paste(subject_rgba, (0, 0), subject_rgba)
    return shadowed_bg


# ---- CLI ------------------------------------------------------------------

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("input")
    parser.add_argument("output")
    parser.add_argument("--bg-color", type=str, default="255,255,255",
                         help="R,G,B for solid background (default white)")
    parser.add_argument("--bg-image", type=str, default=None,
                         help="Path to a background image instead of solid color")
    parser.add_argument("--model", type=str, default="u2net",
                         help="rembg model name, e.g. isnet-general-use, birefnet-general")
    args = parser.parse_args()

    with open(args.input, "rb") as f:
        input_bytes = f.read()
    subject = extract_subject(input_bytes, model_name=args.model)
    shadow = build_dual_shadow(subject)

    if args.bg_image:
        background = Image.open(args.bg_image)
    else:
        r, g, b = map(int, args.bg_color.split(","))
        background = Image.new("RGBA", subject.size, (r, g, b, 255))

    result = composite(subject, shadow, background)
    result.convert("RGB").save(args.output, quality=95)
    print(f"Saved: {args.output}")


if __name__ == "__main__":
    main()