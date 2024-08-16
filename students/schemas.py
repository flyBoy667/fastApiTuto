from typing import Optional

from pydantic import BaseModel


class Student(BaseModel):
    name: str
    lastname: str
    age: int


class UpdateStudent(BaseModel):
    name: Optional[str] = None
    lastname: Optional[str] = None
    age: Optional[int] = None
