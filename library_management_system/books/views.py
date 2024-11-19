from django.shortcuts import redirect, render, get_object_or_404
from django.urls import reverse_lazy, reverse
from django.utils import timezone
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.views.generic import ListView, CreateView, UpdateView, DeleteView, TemplateView
from datetime import timedelta
from books.forms import BookForm, BorrowBookForm
from books.models import BooksModel, BorrowedBook
# Imports for analytics
from datetime import datetime
from django.db.models import Count
from django.db.models.functions import TruncMonth
import json


# About Page - Static Page, using TemplateView
class AboutView(TemplateView):
    template_name = 'about.html'
    extra_context = {'title': "About Page"}  # Provides extra context for template


# Book List View - Shows available books
class BookListView(LoginRequiredMixin, ListView):
    model = BooksModel
    template_name = 'index.html'
    context_object_name = 'books'

    def get_queryset(self):
        return BooksModel.objects.filter(status='available')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['total_books'] = BooksModel.objects.count()  # Total book count for template
        return context


# Custom mixin for superuser restriction
class SuperuserRequiredMixin(UserPassesTestMixin):
    def test_func(self):
        return self.request.user.is_superuser  # Allows only superuser access


# Book Create View - Allows superusers to add a new book
class BookCreateView(LoginRequiredMixin, SuperuserRequiredMixin, CreateView):
    model = BooksModel
    form_class = BookForm
    template_name = "add_book.html"
    success_url = reverse_lazy("index")  # Redirect after successful form submission


# Book Edit View - Allows superusers to edit book details
class BookEditView(LoginRequiredMixin, SuperuserRequiredMixin, UpdateView):
    model = BooksModel
    form_class = BookForm
    template_name = "edit.html"
    success_url = reverse_lazy("index")

    def get_object(self, queryset=None):
        return get_object_or_404(BooksModel, pk=self.kwargs['pk'])


# Book Delete View - Allows superusers to delete a book
class BookDeleteView(LoginRequiredMixin, SuperuserRequiredMixin, DeleteView):
    model = BooksModel
    template_name = 'delete.html'
    success_url = reverse_lazy("index")

    def get_object(self, queryset=None):
        return get_object_or_404(BooksModel, pk=self.kwargs['pk'])


# Borrow Book View - Allows users to borrow an available book
class BookBorrowView(LoginRequiredMixin, CreateView):
    model = BorrowedBook
    form_class = BorrowBookForm
    template_name = 'borrow_book.html'

    def form_valid(self, form):
        book = get_object_or_404(BooksModel, pk=self.kwargs['pk'])

        # Check if the book is available for borrowing
        if book.status != 'available':
            return self.render_to_response(self.get_context_data(form=form, book=book, error='This book is currently not available for borrowing.'))

        # Update the status of the book to 'rent'
        book.status = 'rent'
        book.save()

        # Set the form instance fields
        form.instance.user = self.request.user
        form.instance.book = book

        return super().form_valid(form)

    def get_success_url(self):
        return reverse('borrowed-books')

@login_required
def return_book(request, book_id):
    # Get the borrowed book record
    borrowed_book = get_object_or_404(BorrowedBook, book_id=book_id, return_date__isnull=True)

    # Update the return date to mark the book as returned
    borrowed_book.return_date = timezone.now()
    borrowed_book.returned = True  # Set the returned flag (if you're using that approach)
    borrowed_book.save()

    # Update the book status back to 'available'
    book = borrowed_book.book
    book.status = 'available'
    book.save()

    return render(request, 'return_book.html', {'borrowed_book': borrowed_book})



# Borrowed Books View - Shows a list of borrowed books and status
class BorrowedBooksView(LoginRequiredMixin, ListView):
    model = BorrowedBook
    template_name = 'borrowed_books.html'
    context_object_name = 'borrowed_books'

    def get_queryset(self):
        return BorrowedBook.objects.filter(user=self.request.user)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        borrowed_books = context['borrowed_books']
        
        overdue_books = []
        due_soon_books = []
        
        # Check due dates and categorize books
        for borrowed in borrowed_books:
            if borrowed.due_date < timezone.now():
                overdue_books.append(borrowed)
            elif borrowed.due_date < timezone.now() + timedelta(days=3):
                due_soon_books.append(borrowed)
        
        context['overdue_books'] = overdue_books
        context['due_soon_books'] = due_soon_books
        return context

@login_required
def borrowing_analytics_view(request):    
    # Group rented books by the month of `date_borrowed`
    books_per_month = BorrowedBook.objects.annotate(
        month=TruncMonth('date_borrowed')
    ).values('month').annotate(total=Count('id')).order_by('month')
    
    # Debugging: Print records to console
    print("Books per month:", books_per_month)

    # Prepare data for frontend
    months = []
    rented_books = []
    for record in books_per_month:
        if record['month']:
            month_name = record['month'].strftime('%B')  # Convert month to readable name
            months.append(month_name)
            rented_books.append(record['total'])

    # Debugging: Print data prepared for rendering
    print("Months:", months)
    print("Rented Books:", rented_books)

    return render(request, 'borrowing_analytics.html', {
        'months': json.dumps(months),
        'rented_books': json.dumps(rented_books),
    })

def popular_analytics_view(request):
    # Most Borrowed Books
    most_borrowed_books = BorrowedBook.objects.values('book__title').annotate(
        total=Count('id')
    ).order_by('-total')[:10]  # Top 10 most borrowed books

    # Most Active Users (Top 10)
    most_active_users = BorrowedBook.objects.values('user__username').annotate(
        total=Count('id')
    ).order_by('-total')[:10]  # Top 10 most active users

    # Prepare data for the charts
    borrowed_books_labels = [book['book__title'] for book in most_borrowed_books]
    borrowed_books_data = [book['total'] for book in most_borrowed_books]

    active_users_labels = [user['user__username'] for user in most_active_users]
    active_users_data = [user['total'] for user in most_active_users]

    return render(request, 'popular_analytics.html', {
        'most_borrowed_books': most_borrowed_books,
        'most_active_users': most_active_users,
        'borrowed_books_labels': json.dumps(borrowed_books_labels),
        'borrowed_books_data': json.dumps(borrowed_books_data),
        'active_users_labels': json.dumps(active_users_labels),
        'active_users_data': json.dumps(active_users_data),
    })


def available_analytics_view(request):
    # Count the number of borrowed books that have not been returned
    borrowed_books_count = BorrowedBook.objects.filter(return_date__isnull=True).count()

    # Count the number of available books (status 'available' and not rented)
    available_books_count = BooksModel.objects.filter(status='available').count()

    # Prepare the data for the chart
    labels = ['Available Books', 'Borrowed Books']
    data = [available_books_count, borrowed_books_count]

    return render(request, 'available_analytics.html', {
        'labels': json.dumps(labels),
        'data': json.dumps(data),
    })


