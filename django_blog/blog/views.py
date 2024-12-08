from django.shortcuts import render
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm
from .forms import CustomUserCreationForm
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserChangeForm

def home_view(request):
   
    return render(request, 'blog/base.html')

def register(request):
    if request.method =="POST":
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect("profile")
        
        else:
            form = CustomUserCreationForm()
        return render(request, "register.html", {"form": form})    
        

def user_login (request):
    if request.method == "POST":
        form = AuthenticationForm(data= request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect("profile")
        else:
            form= AuthenticationForm()
        return render(request, "login.html", {"form": form})

def user_logout(request):
    logout(request)
    return redirect ("login") 

@login_required 
def profile(request):
    return render (request, "profile.html", {"user": request.user})


@login_required
def profile(request):
    if request.method == "POST":
        form = UserChangeForm(request.POST, isinstance= request.user)
        if form.is_valid():
            form.save()
            return redirect("profile")
        else:
            form = UserChangeForm(isinstance = request.user)
        return render (request, "profile.html", {"form": form})