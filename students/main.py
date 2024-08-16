import uvicorn
from fastapi import FastAPI, Depends, HTTPException, status
from sqlalchemy.orm import Session

from students.hashing import bcrypt
from . import schemas, models
from Database.database import engine, get_db
from typing import List

# Migration
models.Base.metadata.create_all(engine)

app = FastAPI()


@app.get("/student", response_model=List[schemas.Student], status_code=status.HTTP_200_OK, tags=["Students"])
def fetch_all_students(db: Session = Depends(get_db)):
    students = db.query(models.Student).all()
    if not students:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="No students found")
    return students


@app.get("/student/{student_id}", status_code=status.HTTP_200_OK, tags=["Students"],
         response_model=schemas.ShowStudent)
def get_student(student_id: int, db: Session = Depends(get_db)):
    student = db.query(models.Student).filter(models.Student.id == student_id).first()
    if not student:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"L'étudiant avec l'id {student_id} n'existe pas")
    return student


@app.post("/student/create", tags=["Students"])
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


@app.put('/student/{student_id}/update', status_code=status.HTTP_202_ACCEPTED, tags=["Students"])
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


@app.delete("/student/{student_id}/delete", status_code=status.HTTP_204_NO_CONTENT, tags=['Students'])
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


@app.post('/account/create', status_code=status.HTTP_202_ACCEPTED, response_model=schemas.Account, tags=['Account'])
def create_account(account: schemas.Account, db: Session = Depends(get_db)):
    hashed_password = bcrypt(account.password)
    account = models.Account(username=account.username, password=hashed_password)
    try:
        db.add(account)
        db.commit()
        db.refresh(account)
        return account
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))


@app.get('/account/{account_id}', status_code=status.HTTP_200_OK, response_model=schemas.ShowAccount, tags=['Account'])
def get_account(account_id: int, db: Session = Depends(get_db)):
    account = db.query(models.Account).filter(models.Account.id == account_id).first()
    if not account:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Account not found")
    return account


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=9000)
