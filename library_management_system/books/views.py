from django.shortcuts import redirect, render, get_object_or_404
from books.forms import BookForm, BorrowBookForm
from books.models import BooksModel, BorrowedBook
from django.contrib.auth.models import User,auth
from django.contrib.auth.decorators import login_required, user_passes_test
from django.utils import timezone
from datetime import timedelta

def index(request):
    books = BooksModel.objects.filter(status='available')
    total = BooksModel.objects.count()
    return render(request, 'index.html', {'books': books, 'total_books': total})

def superuser_required(function):
    return user_passes_test(lambda u: u.is_superuser)(function)

def add_book(request):
    if request.method == "POST":
        form = BookForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("index")
    else:
        form = BookForm()
    return render(request, "add_book.html", {"form": form})

@login_required
def borrow_book(request, book_id):
    book = get_object_or_404(BooksModel, pk=book_id)

    if book.status != 'available':
        return render(request, 'borrow_book.html', {
            'form': None,
            'book': book,
            'error': 'This book is currently not available for borrowing.'
        })

    if request.method == 'POST':
        borrowed_book = BorrowedBook(user=request.user, book=book)
        borrowed_book.save()

        book.status = 'rented'
        book.save()

        return redirect('borrowed_books')
    else:
        form = BorrowBookForm()

    return render(request, 'borrow_book.html', {'form': form, 'book': book})


@login_required
def return_book(request, borrowed_id):
    borrowed_book = get_object_or_404(BorrowedBook, id=borrowed_id)

    if request.method == 'POST':
        borrowed_book.book.status = 'available'
        borrowed_book.book.save() 
        
        borrowed_book.return_date = timezone.now() 
        borrowed_book.save()  

        return redirect('borrowed_books')

    return render(request, 'return_book.html', {'borrowed_book': borrowed_book})


@login_required
def borrowed_books(request):
    borrowed_books = BorrowedBook.objects.filter(user=request.user)
    overdue_books = []
    due_soon_books = []

    # Determine if books are overdue or due soon
    for borrowed in borrowed_books:
        if borrowed.due_date < timezone.now():
            overdue_books.append(borrowed)
        elif borrowed.due_date < timezone.now() + timedelta(days=3):
            due_soon_books.append(borrowed)

    context = {
        'borrowed_books': borrowed_books,
        'overdue_books': overdue_books,
        'due_soon_books': due_soon_books,
    }
    return render(request, 'borrowed_books.html', context)

@superuser_required
@login_required
def edit_book(request, book_id):
    book = get_object_or_404(BooksModel, pk=book_id)
    if request.method == "POST":
        form = BookForm(request.POST, instance=book)
        if form.is_valid():
            form.save()
            return redirect("index")
    else:
        form = BookForm(instance=book)
    return render(request, "edit.html", {"form": form, "book": book})

@superuser_required
@login_required
def delete_book(request, book_id):
    book = get_object_or_404(BooksModel, pk=book_id)
    if request.method == 'POST':
        book.delete()
        return redirect('index')
    return render(request, 'delete.html', {'book': book})

