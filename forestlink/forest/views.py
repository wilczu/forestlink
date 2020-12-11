from django.shortcuts import render, redirect
from django.urls import reverse
from django.db import IntegrityError
from django.contrib.auth import authenticate, login, logout

from .models import User

# Create your views here.
def index(request):
    return render(request, "forest/index.html")


def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username = username, password = password)
        
        if user is not None:
            login(request, user)
            return redirect(reverse("index"))
        else:
            return render(request, "forest/login.html", {
                "error": "Invalid username or password!"
            })
    else:
        return render(request, "forest/login.html")


def logout_view(request):
    logout(request)
    return redirect(reverse("index"))


def register_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']
        confirmpassword = request.POST['confirmpassword']

        if password != confirmpassword:
            return render(request, "forest/register.html", {
                "error": "Your passwords must match."
            })

        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "forest/register.html", {
                "error": "This username is taken, please use different one"
            })

        login(request, user)
        return redirect(reverse("index"))
    else:  
        return render(request, "forest/register.html")

