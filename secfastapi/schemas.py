from pydantic import BaseModel, Field, field_validator
from typing import Optional
from datetime import date

class ValidationBase(BaseModel):
    @field_validator("year", check_fields=False)
    def validate_year(cls, value:int):
        current_year = date.today().year
        if value > current_year:
            raise ValueError(f"The year {value} is in the future. Please provide a valid publication year.")
        return value

    @field_validator("status", check_fields=False)
    def validate_status(cls, value:str):
        allowed_statuses = ["available", "rent", "reserved"]
        if value not in allowed_statuses:
            raise ValueError(f"Status '{value}' is invalid. Allowed statuses are: {', '.join(allowed_statuses)}.")
        return value


class AuthorBase(BaseModel):
    name: str
    bio: Optional[str] = None

class AuthorCreate(AuthorBase):
    pass

class AuthorUpdate(BaseModel):
    name: Optional[str] = None
    bio: Optional[str] = None

class Author(AuthorBase):
    author_id: int
    registration_date: date

    class Config:
        from_attributes = True # Allows Pydantic to create models directly from SQLAlchemy objects.
        json_encoders = { date: lambda v: v.isoformat(),} # Converts date into ISO format for serialization

class BookBase(ValidationBase):
    title: str
    author_id: Optional[int] = None
    year: int = Field(..., description="Year of publication (cannot be in the future)")
    summary: str
    category: str
    status: str = "available"

class BookCreate(BookBase):
    pass

class BookUpdate(ValidationBase):
    title: Optional[str] = None
    author_id: Optional[int] = None
    year: Optional[int] = None
    summary: Optional[str] = None
    category: Optional[str] = None
    status: Optional[str] = None


class Book(BookBase):
    book_id: int
    registration_date: date

    class Config:
        from_attributes = True
        json_encoders = { date: lambda v: v.isoformat(),}
