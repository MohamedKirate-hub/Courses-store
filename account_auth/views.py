from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.forms import AuthenticationForm
from .forms import RegisterForm

def logout_view(request):
    logout(request)
    return redirect('home')

def login_view(request):
    page = 'login'
    form = AuthenticationForm()
    if request.method == 'POST':
        form = AuthenticationForm(request, request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(request, username=username, password=password)
            if user:
                login(request, user)
                return redirect('home')
    context = {'form': form, 'page': page}
    return render(request, 'login_register.html', context)

def register_view(request):
    page = 'register'
    form = RegisterForm()
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('home')
    context = {'form': form, 'page': page}
    return render(request, 'login_register.html', context)

def home_page(request):
    return render(request, 'home.html')
