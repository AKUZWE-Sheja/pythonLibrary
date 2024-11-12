from django.shortcuts import redirect, render, get_object_or_404
from django.urls import reverse_lazy, reverse
from django.utils import timezone
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.views.generic import ListView, CreateView, UpdateView, DeleteView, TemplateView
from datetime import timedelta
from books.forms import BookForm, BorrowBookForm
from books.models import BooksModel, BorrowedBook

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
        # Access the book using the primary key from the URL
        book = get_object_or_404(BooksModel, pk=self.kwargs['pk'])

        # Check if the book is available
        if book.status != 'available':
            return self.render_to_response(self.get_context_data(form=form, book=book, error='This book is currently not available for borrowing.'))

        # Update book status to rented and save
        book.status = 'rented'
        book.save()

        # Set the user and book instance in the form
        form.instance.user = self.request.user
        form.instance.book = book
        return super().form_valid(form)

    def get_success_url(self):
        return reverse('borrowed-books')

@login_required
def return_book(request, borrowed_id):
    borrowed_book = get_object_or_404(BorrowedBook, id=borrowed_id)

    if request.method == 'POST':
        borrowed_book.book.status = 'available'
        borrowed_book.book.save() 
        
        borrowed_book.return_date = timezone.now() 
        borrowed_book.save()  

        return redirect('borrowed-books')

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
