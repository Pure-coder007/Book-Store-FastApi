from .database import Base
from datetime import datetime
from sqlalchemy import Column, Integer, String, Boolean, ForeignKey, DateTime
from sqlalchemy.orm import relationship




class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True)
    first_name = Column(String, nullable=False)
    last_name = Column(String, nullable=False)
    email = Column(String, nullable=False, unique=True)
    password = Column(String, nullable=False)
    wallet_balance = Column(Integer, default=0)
    created_at = Column(DateTime, default=datetime.utcnow)
    selected_books = relationship("SelectedBooks", back_populates="user")

class SelectedBooks(Base):
    __tablename__ = "selected_books"

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    name = Column(String, nullable=False)
    genre = Column(String, nullable=False)
    price = Column(Integer, nullable=False)
    time_added = Column(DateTime, default=datetime.utcnow)
    user = relationship("User", back_populates="selected_books")



# Giving book reviews
class Reviews(Base):
    __tablename__ = "reviews"

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    book_id = Column(Integer, ForeignKey("selected_books.id"))
    book_name = Column(String, nullable=False)
    review = Column(String, nullable=False)
    stars = Column(Integer, nullable=False)
    review_time = Column(DateTime, default=datetime.utcnow)
    user = relationship("User", back_populates="reviews")
    book = relationship("SelectedBooks", back_populates="reviews")