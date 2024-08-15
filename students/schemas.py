from pydantic import BaseModel


class Student(BaseModel):
    name: str
    lastname: str
    age: int
