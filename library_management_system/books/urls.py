from django.urls import path
from .views import AboutView, BookListView, BookCreateView, BookEditView, BookDeleteView, BookBorrowView, BorrowedBooksView
from . import views

urlpatterns = [
    path('about/', AboutView.as_view(), name="book-about"),
    path('', BookListView.as_view(), name="index"),
    path('book/add/', BookCreateView.as_view(), name="book-add"),
    path('book/<int:pk>/edit/', BookEditView.as_view(), name="book-edit"),
    path('book/<int:pk>/delete/', BookDeleteView.as_view(), name="book-delete"),
    path('book/<int:pk>/borrow/', BookBorrowView.as_view(), name='book-borrow'),
    # path('borrowed/<int:pk>/return/', BookReturnView.as_view(), name='book-return'),
    path('book/<int:borrowed_id>/return/', views.return_book, name='book-return'),
    path('books/borrowed/', BorrowedBooksView.as_view(), name="borrowed-books"),
    path('analytics1/', views.borrowing_analytics_view, name='borrowing_analytics'),
    path('popular-analytics/', views.popular_analytics_view, name='popular_analytics'),
    path('available-analytics/', views.available_analytics_view, name='available_analytics'),
]
