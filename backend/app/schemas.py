from pydantic import BaseModel, EmailStr
from typing import Optional

class EmployeeBase(BaseModel):
    first_name: str
    last_name: str
    email: EmailStr
    department: str
    salary: float

class EmployeeCreate(EmployeeBase):
    pass

class Employee(EmployeeBase):
    id: int

    class Config:
        from_attributes = True
