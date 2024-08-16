import uvicorn
from fastapi import FastAPI, Depends, HTTPException, status
from sqlalchemy.orm import Session
from . import schemas, models
from Database.database import engine, get_db
from typing import List

# Migration
models.Base.metadata.create_all(engine)

app = FastAPI()


@app.get("/")
def index():
    return {"message": "Hello World"}


@app.get("/student", response_model=List[schemas.Student], status_code=status.HTTP_200_OK)
def fetch_all_students(db: Session = Depends(get_db)):
    students = db.query(models.Student).all()
    if not students:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="No students found")
    return students


@app.get("/student/{student_id}", status_code=status.HTTP_200_OK)
def get_student(student_id, db: Session = Depends(get_db)):
    try:
        student = db.query(models.Student).filter(models.Student.id == student_id).first()
        if not student:
            raise ValueError
    except ValueError:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"L'etudiant avec l'id {student_id} n'existe pas")
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))

    return student


@app.post("/student/create")
def create(request: schemas.Student, db: Session = Depends(get_db)):
    student = models.Student(**request.dict())
    try:
        db.add(student)
        db.commit()
        db.refresh(student)
        return student
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))


@app.put('/student/{student_id}/update', status_code=status.HTTP_202_ACCEPTED)
def update(student_id, request: schemas.UpdateStudent, db: Session = Depends(get_db)):
    student = db.query(models.Student).filter(models.Student.id == student_id)
    if not student.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"L'etudiant avec l'id {student_id} n'existe pas")

    update_data = request.dict(exclude_unset=True)
    student.update(update_data, synchronize_session='evaluate')

    try:
        db.commit()
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))

    return {"message": "Student updated successfully"}


@app.delete("/student/{student_id}/delete", status_code=status.HTTP_204_NO_CONTENT)
def destroy(student_id, db: Session = Depends(get_db)):
    student_row_count = db.query(models.Student).filter(models.Student.id == student_id).delete(
        synchronize_session='evaluate')
    if student_row_count == 0:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"L'etudiant avec l'id {student_id} n'existe pas")
    else:
        try:
            db.commit()
        except Exception as e:
            db.rollback()
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=9000)
