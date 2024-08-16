from typing import List

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from services import student
from Database.database import get_db
from students import schemas, models

router = APIRouter(
    tags=['Students'],
    prefix='/api/student',
)


@router.get("/", response_model=List[schemas.Student], status_code=status.HTTP_200_OK, tags=["Students"])
def fetch_all_students(db: Session = Depends(get_db)):
    return student.fetch_all_students(db)


@router.get("/{student_id}", status_code=status.HTTP_200_OK, response_model=schemas.ShowStudent)
def get_student(student_id: int, db: Session = Depends(get_db)):
    return student.get_student(student_id, db)


@router.post("/create", )
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


@router.put('/{student_id}/update', status_code=status.HTTP_202_ACCEPTED, )
def update(student_id: int, request: schemas.UpdateStudent, db: Session = Depends(get_db)):
    student = db.query(models.Student).filter(models.Student.id == student_id)
    if not student.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"L'étudiant avec l'id {student_id} n'existe pas")

    update_data = request.dict(exclude_unset=True)
    student.update(update_data)

    try:
        db.commit()
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))

    return {"message": "Student updated successfully"}


@router.delete("/{student_id}/delete", status_code=status.HTTP_204_NO_CONTENT, tags=['Students'])
def destroy(student_id: int, db: Session = Depends(get_db)):
    student_row_count = db.query(models.Student).filter(models.Student.id == student_id).delete()
    if student_row_count == 0:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"L'étudiant avec l'id {student_id} n'existe pas")
    else:
        try:
            db.commit()
        except Exception as e:
            db.rollback()
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))
