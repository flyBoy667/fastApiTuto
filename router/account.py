from typing import List

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from Database.database import get_db
from students import models, schemas
from students.hashing import bcrypt

router = APIRouter(
    tags=['Account'],
    prefix='/api/account',
)


@router.post('/create', status_code=status.HTTP_202_ACCEPTED, response_model=schemas.Account)
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


@router.get('/{account_id}', status_code=status.HTTP_200_OK, response_model=schemas.ShowAccount)
def get_account(account_id: int, db: Session = Depends(get_db)):
    account = db.query(models.Account).filter(models.Account.id == account_id).first()
    if not account:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Account not found")
    return account
