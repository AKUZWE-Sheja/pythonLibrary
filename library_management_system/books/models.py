from django.db import models
from django.contrib.auth.models import User
from datetime import timedelta
from django.utils import timezone


class Author(models.Model):
    author_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100, unique=True) 
    bio = models.TextField(null=True, blank=True)  # Optional
    registration_date = models.DateField(auto_now_add=True)

    def __str__(self):
        return self.name
    
    class Meta:
        ordering = ['name']  # Ascending order
        db_table = 'authors'


class BooksModel(models.Model):
    STATUS_CHOICES = [
        ('available', 'Available'),
        ('rent', 'Rent'),
        ('missing', 'Missing'),
    ]

    GENRE_CHOICES = [
        ('fiction', 'Fiction'),
        ('non_fiction', 'Non-Fiction'),
        ('romance', 'Romance'),
        ('classic', 'Classic'),
        ('dystopian', 'Dystopian Fiction'),
        ('historical', 'Historical Fiction'),
        ('biography', 'Biography'),
        ('mystery', 'Mystery'),
        ('science_fiction', 'Science Fiction'),
        ('fantasy', 'Fantasy'),
    ]

    book_id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=80)
    author = models.ForeignKey(Author, on_delete=models.SET_NULL, null=True, blank=True)
    year = models.IntegerField()
    summary = models.TextField()
    category = models.CharField(max_length=50, choices=GENRE_CHOICES) 
    registration_date = models.DateField(auto_now_add=True)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='available')

    def __str__(self):
        return self.title

    def delete(self, *args, **kwargs):
        # Handle file deletion here if needed
        # self.pdf.delete()  # Uncomment if there's a pdf field
        super().delete(*args, **kwargs)  # Ensure parent delete method is called

    def borrow(self, user):
        if self.status == 'available':
            self.status = 'rent'
            self.save()
            BorrowedBook.objects.create(book=self, user=user)  # Make sure BorrowedBook model is defined
        else:
            raise Exception("This book is currently unavailable.")

    class Meta:
        ordering = ['title']  # Ascending order
        db_table = 'library_books'


class BorrowedBook(models.Model):
    book = models.ForeignKey(BooksModel, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    date_borrowed = models.DateTimeField(default=timezone.now)
    due_date = models.DateTimeField()
    return_date = models.DateTimeField(null=True, blank=True)
    duration_days = models.IntegerField(default=14)

    def __str__(self):
        return f"{self.user.username} borrowed {self.book.title}"

    def save(self, *args, **kwargs):
        if not self.due_date:
            self.due_date = self.date_borrowed + timedelta(days=self.duration_days)
        super().save(*args, **kwargs)
