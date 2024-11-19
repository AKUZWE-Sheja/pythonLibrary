from sqlalchemy.orm import Session  # type: ignore
from models import Author, Book
from schemas import AuthorCreate, AuthorUpdate, BookCreate, BookUpdate

# Authors

def get_authors(db: Session, skip: int = 0, limit: int = 10):
# Fetch all authors with pagination.
    return db.query(Author).offset(skip).limit(limit).all()


def get_author(db: Session, author_id: int):
# Fetch a single author by ID.
    return db.query(Author).filter(Author.author_id == author_id).first()

def create_author(db: Session, author: AuthorCreate):
    db_author = Author(name=author.name, bio=author.bio)
    db.add(db_author)
    db.commit()
    db.refresh(db_author)
    return db_author

def update_author(db: Session, author_id: int, author_update: AuthorUpdate):
    db_author = db.query(Author).filter(Author.author_id == author_id).first()
    if not db_author:
        return None
    for key, value in author_update.dict(exclude_unset=True).items():
        setattr(db_author, key, value)
    db.commit()
    db.refresh(db_author)
    return db_author


def delete_author(db: Session, author_id: int):
# Delete an author by ID.
    db_author = db.query(Author).filter(Author.author_id == author_id).first()
    if db_author:
        db.delete(db_author)
        db.commit()
        return db_author
    return None


# Books

def get_books(db: Session, skip: int = 0, limit: int = 10):
# Fetch all books with pagination.
    return db.query(Book).offset(skip).limit(limit).all()

def get_book(db: Session, book_id: int):
# Fetch a single book by ID.
    return db.query(Book).filter(Book.book_id == book_id).first()


def create_book(db: Session, book: BookCreate):
    db_book = Book(
        title=book.title,
        author_id=book.author_id,
        year=book.year,
        summary=book.summary,
        category=book.category,
        status=book.status
    )
    db.add(db_book)
    db.commit()
    db.refresh(db_book)
    return db_book


def update_book(db: Session, book_id: int, book_update: BookUpdate):
    db_book = db.query(Book).filter(Book.book_id == book_id).first()
    if not db_book:
        return None
    for key, value in book_update.dict(exclude_unset=True).items():
        setattr(db_book, key, value)
    db.commit()
    db.refresh(db_book)
    return db_book


def delete_book(db: Session, book_id: int):
    db_book = db.query(Book).filter(Book.book_id == book_id).first()
    if db_book:
        db.delete(db_book)
        db.commit()
        return db_book
    return None

def get_book_by_name(db: Session, title: str):
    return db.query(Book).filter(Book.title == title).first()
