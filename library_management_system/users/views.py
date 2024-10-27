from django.shortcuts import render, redirect
from .forms import UserRegisterForm
from django.contrib import messages

def register(request):
    if request.method == "POST":
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            messages.success(request, f'Account successfully created for {username}. You can now log in!')
            return redirect("login")
        else:
            messages.error(request, "Please correct the errors below.")  # Inform user of form errors
    else:
        form = UserRegisterForm()
    return render(request, 'register.html', {'form': form})
