from fastapi import HTTPException, status

from students import models


def fetch_all_students(db):
    students = db.query(models.Student).all()
    if not students:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="No students found")
    return students


def get_student(student_id, db):
    student = db.query(models.Student).filter(models.Student.id == student_id).first()
    if not student:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"L'étudiant avec l'id {student_id} n'existe pas")
    return student
