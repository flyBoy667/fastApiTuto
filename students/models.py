from Database.database import Base
from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship


class Student(Base):
    __tablename__ = "students"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255))
    lastname = Column(String(255))
    age = Column(Integer)
    accounts = relationship("Account", back_populates="student")


class Account(Base):
    __tablename__ = "accounts"
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(255))
    password = Column(String(255))
    student_id = Column(Integer, ForeignKey("students.id"))
    student = relationship("Student", back_populates="accounts")
