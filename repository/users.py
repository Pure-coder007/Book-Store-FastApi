from sqlalchemy.orm import Session
import models, schemas, oauth2
from fastapi import HTTPException, status, Depends
from password_hash import Hash
from sqlalchemy.exc import IntegrityError




def create_user(request: schemas.CreateUser, db: Session):
    try:
        new_user = models.User(
            first_name = request.first_name,
            last_name = request.last_name,
            email = request.email,
            password = Hash.bcrypt(request.password)
        )
        if new_user.email in db.query(models.User.email).all():
            return {"detail": "User with this email already exists"}
            # raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="User with this email already exists")
        db.add(new_user)
        db.commit()
        db.refresh(new_user)
        return new_user
    except IntegrityError:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="User with this email already exists")


def get_user(email: str, db: Session, current_user: models.User):
    if email != current_user.email:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="You are not permitted to see this profile")
    
    user = db.query(models.User).filter(models.User.email == email).first()
    
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    
    return user


def update_user(request: schemas.UpdateUser, db: Session, current_user: models.User):
    user = db.query(models.User).filter(models.User.email == current_user.email).first()
    user.first_name = request.first_name
    user.last_name = request.last_name
    user.email = request.email
    db.commit()
    db.refresh(user)
    return user



def update_wallet_balance(request: schemas.UpdateWallet, db: Session, current_user: models.User):
    user = db.query(models.User).filter(models.User.email == current_user.email).first()

    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    # Calculate the new balance
    new_balance = user.wallet_balance + request.wallet

    # Update the wallet balance
    user.wallet_balance = new_balance
    db.commit()
    db.refresh(user)

     # Format the balance with a comma if it is up to 4 digits
    formatted_balance = f"{user.wallet_balance:,.2f}" if user.wallet_balance >= 1000 else f"{user.wallet_balance:.2f}"

    print(user.wallet_balance, 'wallet balance')
    return {"message": "Wallet balance updated", "wallet_balance":"#" + formatted_balance}