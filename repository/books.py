from sqlalchemy.orm import Session
import models, schemas, database, logging, oauth2
from fastapi import HTTPException, status, Depends
from oauth2 import get_current_user
from fastapi.security import OAuth2PasswordBearer
from jose import jwt, JWTError
from available_books import books
from datetime import datetime


# print(books, '556678897754435678908765432345678654')


logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)



def get_all_books():
    return books



# Adding books to cart
def add_to_cart(title, db, user_id):
    for book in books:
        if book.get("title") == title:
            price = book.get("price") if book.get("price") is not None else 0
            quantity = book.get("quantity") if book.get("quantity") is not None else 1
            
            selected_book = models.SelectedBooks(
                user_id=user_id,
                name=book.get("title"),
                genre=book.get("genre"),
                price=price,
                time_added=datetime.utcnow(),
                author=book.get("author"),
                quantity=quantity,
                total_price=price * quantity
            )
            
            # Checking if the book is already in the cart so I can increment the quantity
            cart = db.query(models.SelectedBooks).filter(
                models.SelectedBooks.user_id == user_id,
                models.SelectedBooks.name == title
            ).first()
            
            if cart:
                cart.quantity += 1
                cart.total_price = cart.price * cart.quantity
                db.commit()
                logger.info(f"Book {title} quantity increased")
                return {
                    "title": cart.name,
                    "author": cart.author,
                    "genre": cart.genre,
                    "price": cart.price,
                    "quantity": cart.quantity,
                    "total_price": cart.total_price
                }
                
            db.add(selected_book)
            db.commit()
            db.refresh(selected_book)
            logger.info(f"Book {title} added to cart")
            return {
                "title": selected_book.name,
                "author": selected_book.author,
                "genre": selected_book.genre,
                "price": selected_book.price,
                "quantity": selected_book.quantity,
                "total_price": selected_book.total_price
            }
            
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Book with title {title} not found")

    


# View selected books
def view_selected_books(db: Session = Depends(database.get_db), current_user: schemas.ShowBooks = Depends(oauth2.get_current_user)):
    selected_books = db.query(models.SelectedBooks).filter(models.SelectedBooks.user_id == current_user.id).all()
    print(selected_books, 'selected ')
    books = [{"name": book.name, "genre": book.genre, "price": book.price, "author": book.author, "time_added": book.time_added.strftime("%Y-%m-%d %H:%M:%S"), "quantity": book.quantity, "total_price": book.price * book.quantity} for book in selected_books]
    if not selected_books:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="No books found in your cart")
    return books



def delete_from_cart(title, db, user_id):
    book = db.query(models.SelectedBooks).filter(models.SelectedBooks.user_id == user_id, models.SelectedBooks.name == title).first()
    if not book:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Book with title {title} not found in your cart")
    db.delete(book)
    db.commit()
    logger.info(f"Book {title} deleted from cart")
    return {"message": f"Book '{title}' deleted from cart"}




# Payment for selected books
def payment_for_selected_books(db: Session = Depends(database.get_db), current_user: schemas.ShowBooks = Depends(oauth2.get_current_user)):

    # Query for the user's selected books in the cart
    selected_books = db.query(models.SelectedBooks).filter(models.SelectedBooks.user_id == current_user.id).all()

    if not selected_books:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="No books found in your cart")

    # Calculate the total price of all selected books
    total_price = sum(book.total_price for book in selected_books)

    # Query for the user's wallet balance
    user = db.query(models.User).filter(models.User.id == current_user.id).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    wallet_balance = user.wallet_balance

    # Check if the user has sufficient funds
    if wallet_balance < total_price:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Insufficient funds in your wallet")

    # Perform the payment by updating the wallet balance and clearing the cart
    new_balance = wallet_balance - total_price
    user.wallet_balance = new_balance
    db.query(models.SelectedBooks).filter(models.SelectedBooks.user_id == current_user.id).delete(synchronize_session=False)
    db.commit()

    logger.info("Payment successful")
    return {"message": "Payment successful", "wallet_balance": new_balance}




# Filter books by author



def filter_books_by_author(author: str):
    filtered_books = [book for book in books if book.get("author") == author]
    if not filtered_books:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"No books found by author {author}")
    return filtered_books