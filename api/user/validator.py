from uuid import UUID, uuid4
from pydantic import BaseModel, EmailStr, Field, computed_field
from typing import Annotated,Literal, Optional


class Patient(BaseModel):
    id: UUID = Field(default_factory=uuid4)

    name: Annotated[
        str,
        Field(
            min_length=3,
            max_length=50,
            description="Name of the patient"
        )
    ]

    age: Annotated[
        int,
        Field(
            gt=0,
            le=120,
            description="Age of the patient"
        )
    ]

    email: EmailStr
    is_married: bool = False
    gender: Annotated[Literal["male", "femail", "other"], Field(description="Gender of the patient")]
    height: float
    weight: float
    
    @computed_field
    @property
    def bmi(self) -> float:
        return self.weight / (self.height ** 2)

class UpdatePatient(BaseModel):
    name: Annotated[Optional[str], Field(default=None, min_length=3, max_length=50)]
    age: Annotated[Optional[int], Field(default=None, gt=0, le=120)]
    email: Optional[EmailStr] = None
    is_married: Optional[bool] = None
    gender: Annotated[
        Optional[Literal["male", "female", "other"]],
        Field(default=None, description="Gender of the patient")
    ]
    height: Optional[float] = Field(default=None, gt=0)
    weight: Optional[float] = Field(default=None, gt=0)