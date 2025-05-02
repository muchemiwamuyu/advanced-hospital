from pydantic import BaseModel, Field
from typing import List

class PatientSchema(BaseModel):
    first_name: str = Field(..., example="John")
    last_name: str = Field(..., example="Doe")
    number: str = Field(..., example="0712345678")
    address: str = Field(..., example="Nairobi")
    medical_history: List[str] = Field(..., example=["diabetes", "hypertension"])
    contact_history: List[str] = Field(..., example=["Jane Doe", "Mike Smith"])
