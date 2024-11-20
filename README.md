# PythonLibrary
A digital library using Python 

## Overview
PythonLibrary is a digital library application designed to facilitate the management of books and borrowing processes. It leverages Django's powerful features to provide a user-friendly interface for both users and administrators.

## Features
- **User Authentication**: Secure access for users and superusers.
- **Book Management**: Superusers can add, edit, and delete books.
- **Borrowing System**: Users can borrow available books and return them.
- **Book Status Tracking**: Real-time tracking of book availability and user borrowing status.
- **Responsive Design**: Mobile-friendly interface for better accessibility.

## Notes
- I had added some CSS, and after removing them, an update did not happen. I solved this by running `python manage.py collectstatic`.
  
- Whitenoise minimizes and compresses static files, while Django Compressor combines multiple static files into one, reducing the number of requests the client makes to the server.

- **Crispy Forms**: Provides easier form rendering, customizable templates, field validation, and integration with Bootstrap.

- The `as_view()` method is specific to class-based views (CBVs), which are a modular way of handling views in Django. If you receive the error `AttributeError: 'function' object has no attribute 'as_view'`, it likely means you are using function-based views (FBVs) without converting them to classes. CBVs (like `ListView`, `DetailView`, `CreateView`, etc.) offer a reusable structure ideal for complex views due to built-in functionality and easy inheritance.

- I encountered difficulties with timezones. In PostgreSQL, I ran `SHOW TIMEZONE;` to check my current timezone and `SET TIMEZONE TO 'UTC';` to set it correctly.

- SQL Injection (SQLi) occurs when code incorrectly constructs SQL queries containing user input. Django's ORM uses parameterized statements everywhere, making it highly resistant to SQLi. Thus, if you’re using the ORM for database queries, your app is likely safe. Example of a vulnerable query:
    ```python
    def search(request):
        cursor = db.cursor()
        cursor.execute(
            "SELECT * FROM some_table WHERE title LIKE '%?%'",
            [request.GET['q']]
        )
    ```



