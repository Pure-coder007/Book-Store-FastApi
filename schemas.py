from pydantic import BaseModel
from typing import Optional, List

class CreateUser(BaseModel):
    first_name: str
    last_name: str
    email: str
    password: str

    class Config:
        orm_mode = True

class ShowUser(BaseModel):
    first_name: str
    last_name: str
    email: str
    wallet_balance: int
    
    class Config:
        orm_mode = True

class Token(BaseModel):
    access_token: str
    token_type: str

    class Config:
        orm_mode = True

class TokenData(BaseModel):
    email: Optional[str] = None

class ShowBooks(BaseModel):
    title: str
    author: str
    genre: str
    price: int

    class Config:
        orm_mode = True

class UpdateUser(BaseModel):
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    email: Optional[str] = None
    
    class Config:
        orm_mode = True

class UpdateWallet(BaseModel):
    wallet: Optional[int] = None

    class Config:
        orm_mode = True

class WalletBalanceResponse(BaseModel):
    message: str
    wallet_balance: str

class AddBook(BaseModel):
    title: str
    # quantity: int 
    
    class Config:
        orm_mode = True

class ShowAddedBooks(BaseModel):
    title: str
    author: str
    genre: str
    price: int
    quantity: int
    total_price: int

    class Config:
        orm_mode = True

class ShowSelectedBooks(BaseModel):
    name: str
    genre: str
    price: int
    time_added: str
    author: str
    quantity: int
    total_price: int

    class Config:
        orm_mode = True
