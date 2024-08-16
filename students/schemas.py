from typing import Optional, List

from pydantic import BaseModel


class Student(BaseModel):
    name: str
    lastname: str
    age: int

    class Config:
        orm_mode = True


class UpdateStudent(Student):
    name: Optional[str] = None
    lastname: Optional[str] = None
    age: Optional[int] = None


class Account(BaseModel):
    username: str
    password: str


class ShowAccount(BaseModel):
    username: str

    class Config:
        orm_mode = True


class ShowStudent(Student):
    accounts: List[ShowAccount] = []

    class Config:
        orm_mode = True
