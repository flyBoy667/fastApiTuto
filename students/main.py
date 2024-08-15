import uvicorn
from fastapi import FastAPI, Depends, HTTPException, status
from sqlalchemy.orm import Session

from Database import database
from . import schemas, models
from Database.database import engine, get_db

# Migration
models.Base.metadata.create_all(engine)

app = FastAPI()


@app.get("/")
def index():
    return {"message": "Hello World"}


@app.get("/student")
def fetch_all_students(db: Session = Depends(get_db)):
    students = db.query(models.Student).all()
    return students


@app.get("/student/{student_id}", status_code=status.HTTP_200_OK)
def show(student_id, db: Session = Depends(get_db)):
    student = db.query(models.Student).filter(models.Student.id == student_id).first()
    if not student:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"L'etudiant avec l'id {student_id} n'existe pas")
    return student


@app.post("/student/create")
def create(request: schemas.Student, db: Session = Depends(get_db)):
    student = models.Student(**request.dict())
    db.add(student)
    db.commit()
    db.refresh(student)
    return student


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=9000)
