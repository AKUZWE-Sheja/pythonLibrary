from django.urls import path
from . import views
from .views import borrow_book, return_book

urlpatterns = [
    path("", views.index, name="index"),
    path("addBook/", views.add_book, name="add_book"),
    path('borrow/<int:book_id>/', borrow_book, name='borrow_book'),
    path('return/<int:borrowed_id>/', return_book, name='return_book'),
    path("borrowed/", views.borrowed_books, name="borrowed_books"),
    path('delete/<int:book_id>/', views.delete_book, name='delete_book'),

]
