from fastapi import APIRouter, status, HTTPException, Depends
import models, schemas, database, oauth2, available_books
from typing import List
from sqlalchemy.orm import Session
from repository.books import get_all_books, add_to_cart, view_selected_books, delete_from_cart, payment_for_selected_books, filter_books_by_author




# print(available_books.books, 'AVAILABLE')


router = APIRouter(
    tags=['Books']
)

def get_db():
    db = database.SessionLocal()
    try:
        yield db
    finally:
        db.close()


def get_all_books():
    return available_books.books




# Getting all books
@router.get("/books", status_code=status.HTTP_200_OK, response_model=List[schemas.ShowBooks])
def all_books(current_user: schemas.ShowBooks = Depends(oauth2.get_current_user)):
    return get_all_books()




# Adding books to cart
@router.post("/books/cart", status_code=status.HTTP_200_OK, response_model=schemas.ShowAddedBooks)
def add_books_to_cart(request: schemas.AddBook, db: Session = Depends(get_db), current_user: schemas.ShowBooks = Depends(oauth2.get_current_user)):
    return add_to_cart(request.title, db, current_user.id)



# View selected books
@router.get("/books/cart", status_code=status.HTTP_200_OK, response_model=List[schemas.ShowSelectedBooks])
def selected_books(db: Session = Depends(database.get_db), current_user: schemas.ShowBooks = Depends(oauth2.get_current_user)):
    print(current_user.id, 'current user')
    return view_selected_books(db, current_user)



# Deleting book from cart
@router.delete("/books/cart/{title}", status_code=status.HTTP_200_OK)
def delete_book_from_cart(title: str, db: Session = Depends(database.get_db), current_user: schemas.ShowBooks = Depends(oauth2.get_current_user)):
    return delete_from_cart(title, db, current_user.id)



# Paying for books
@router.post("/books/cart/payment", status_code=status.HTTP_200_OK)
def payment_for_books(db: Session = Depends(database.get_db), current_user: schemas.ShowBooks = Depends(oauth2.get_current_user)):
    return payment_for_selected_books(db, current_user)




# Filter books by author
@router.get("/books/author", response_model=List[schemas.ShowBooks])
def get_books_by_author(author: str):
    return filter_books_by_author(author)