from fastapi import APIRouter, status, Depends, HTTPException, Query
import models, schemas, database, oauth2
from sqlalchemy.orm import Session
from password_hash import Hash
from typing import List, Optional
from database import engine, SessionLocal
from repository import users as userRepository


router = APIRouter(
    prefix="/users",
    tags=['Users']
)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# Creating a user
@router.post("/", status_code=status.HTTP_201_CREATED, response_model=schemas.CreateUser)
def create(request: schemas.CreateUser, db: Session = Depends(get_db)):
    return userRepository.create_user(request, db)


# Seeing my User Profile
@router.get("/", status_code=status.HTTP_200_OK, response_model=schemas.ShowUser)
def show_my_profile(email: Optional[str] = Query(None), db: Session = Depends(get_db), current_user: schemas.ShowUser = Depends(oauth2.get_current_user)):
    if not email:
        email = current_user.email
    return userRepository.get_user(email, db, current_user)




# Updating the user profile
@router.put("/", status_code=status.HTTP_202_ACCEPTED, response_model=schemas.UpdateUser)
def update_my_profile(request: schemas.UpdateUser, db: Session = Depends(get_db), current_user: schemas.UpdateUser = Depends(oauth2.get_current_user)):
    return userRepository.update_user(request, db, current_user)



# Update Wallet Balance
@router.put("/wallet", status_code=status.HTTP_202_ACCEPTED, response_model=schemas.WalletBalanceResponse)
def update_wallet_balance(request: schemas.UpdateWallet, db: Session = Depends(get_db), current_user: schemas.UpdateWallet = Depends(oauth2.get_current_user)):
    
    return userRepository.update_wallet_balance(request, db, current_user)
