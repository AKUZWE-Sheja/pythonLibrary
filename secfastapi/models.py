from sqlalchemy import Column, Integer, String, Text, ForeignKey, Date, Enum, func
from sqlalchemy.orm import relationship, declarative_base

Base = declarative_base()

class Author(Base):
    __tablename__ = 'authors'
    author_id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), unique=True, index=True)
    bio = Column(Text, default='' ,nullable=True)
    registration_date = Column(Date, default=func.now())

    books = relationship("Book", back_populates="author")

    def __str__(self):
        return self.name

class Book(Base):
    __tablename__ = 'library_books'
    book_id = Column(Integer, primary_key=True, index=True)
    title = Column(String(80), index=True)
    author_id = Column(Integer, ForeignKey('authors.author_id'), nullable=True)
    year = Column(Integer)
    summary = Column(Text)
    category = Column(String(50))
    registration_date = Column(Date, default=func.now())
    status = Column(String(10), default='available')

    author = relationship("Author", back_populates="books")

    def __str__(self):
        return self.title
