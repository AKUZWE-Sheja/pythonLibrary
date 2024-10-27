from django.db import models
from django.contrib.auth.models import User
from datetime import timedelta
from django.utils import timezone

# Create your models here.
class BooksModel(models.Model): 
    STATUS_CHOICES = [
        ('available', 'Available'),
        ('rent', 'Rent'),
        ('missing', 'Missing'),
    ]

    book_id = models.AutoField(primary_key=True)
    title = models.CharField(max_length = 80)
    author = models.CharField(max_length=80)
    year = models.CharField(max_length=80)
    summary = models.TextField(max_length=2000)
    category = models.CharField(max_length=80)
    author_id = models.IntegerField(default=0)
    # pdf = models.FileField(upload_to='pdfs/') #I willuse it later
    registration_date = models.DateField(auto_now_add=True)
    # isbn = models.CharField(max_length=10)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='available')

    def __str__(self):
        return self.title
    
    def delete(self, *args, **kwargs):
        self.pdf.delete()
        super().delete(*args, **kwargs) # Calling the delete method of the parent class (models.Model). It removes the instance from the database. Using super() ensures that any additional cleanup or functionality defined in the parent class's delete method is also executed.


    def borrow(self, user):
        if self.status == 'available':
            self.status = 'rent'
            self.save()
            BorrowedBook.objects.create(book=self, user=user)
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
