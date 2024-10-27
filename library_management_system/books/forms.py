from django import forms
from .models import BooksModel, BorrowedBook

class BookForm(forms.ModelForm):
    class Meta:
        model = BooksModel
        fields = '__all__'

class BorrowBookForm(forms.ModelForm):
    class Meta:
        model = BorrowedBook
        fields = ['duration_days']  

    duration_days = forms.IntegerField(
        label='Duration (in days)',
        min_value=1,  
        initial=14    
    )
