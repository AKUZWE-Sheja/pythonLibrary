from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session # type: ignore
import models, schemas, crud
from connection import engine, SessionLocal

models.Base.metadata.create_all(bind=engine)

app = FastAPI()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.post("/authors/", response_model=schemas.Author)
def create_author(author: schemas.AuthorCreate, db: Session = Depends(get_db)):
    return crud.create_author(db=db, author=author)

@app.get("/authors/", response_model=list[schemas.Author])
def read_authors(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    authors = crud.get_authors(db, skip=skip, limit=limit)
    return authors

@app.get("/authors/{author_id}", response_model=schemas.Author)
def read_author(author_id: int, db: Session = Depends(get_db)):
    author = crud.get_author(db=db, author_id=author_id)
    if author is None:
        raise HTTPException(status_code=404, detail="Author not found")
    return author

@app.put("/authors/{author_id}", response_model=schemas.Author)
def update_author(author_id: int, updated_data: schemas.AuthorUpdate, db: Session = Depends(get_db)):
    return crud.update_author(db=db, author_id=author_id, author_update=updated_data)

@app.delete("/authors/{author_id}")
def delete_author(author_id: int, db: Session = Depends(get_db)):
    crud.delete_author(db=db, author_id=author_id)
    return {"message": "Author deleted successfully"}


# Book Endpoints

@app.post("/books/", response_model=schemas.Book)
def create_book(book: schemas.BookCreate, db: Session = Depends(get_db)):
    return crud.create_book(db=db, book=book)

@app.get("/books/", response_model=list[schemas.Book])
def read_books(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    return crud.get_books(db=db, skip=skip, limit=limit)

@app.get("/books/{book_id}", response_model=schemas.Book)
def read_book(book_id: int, db: Session = Depends(get_db)):
    book = crud.get_book_by_id(db=db, book_id=book_id)
    if book is None:
        raise HTTPException(status_code=404, detail="Book not found")
    return book

@app.get("/books/title/{title}", response_model=schemas.Book)
def read_book_by_title(title: str, db: Session = Depends(get_db)):
    book = crud.get_book_by_title(db=db, title=title)
    if book is None:
        raise HTTPException(status_code=404, detail="Book not found")
    return book

@app.put("/books/{book_id}", response_model=schemas.Book)
def update_book(book_id: int, updated_data: schemas.BookUpdate, db: Session = Depends(get_db)):
    return crud.update_book(db=db, book_id=book_id, book_update=updated_data)

@app.delete("/books/{book_id}")
def delete_book(book_id: int, db: Session = Depends(get_db)):
    crud.delete_book(db=db, book_id=book_id)
    return {"message": "Book deleted successfully"}
