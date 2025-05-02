from pydantic import BaseModel, Field
from typing import List
from enum import Enum
import bcrypt

class roleEnum(str, Enum):
    admin = "admin",
    doctor = "doctor",
    nurse = "nurse",
    lab_tech = "lab_tech",
    environment = "janitor, clean_scedhule" # for small departments
    support = "support"



class UserSchema(BaseModel):
    first_name: str = Field(..., examples="Jay"),
    last_name: str = Field(..., examples="mark"),
    number: str = Field(..., examples="0723456787"),
    role: roleEnum = Field(..., examples="doctor")
    staff_id: str = Field(..., examples="NOV-3445")
    password: str = Field(..., examples="doe@4893")

def hash_password(self):
    # hashes the users password
    self.password = bcrypt.hashpw(self.password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')

def check_password(self, password: str):
        """Checks if the provided password matches the stored password"""
        return bcrypt.checkpw(password.encode('utf-8'), self.password.encode('utf-8'))