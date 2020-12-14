from django.shortcuts import render, redirect, HttpResponse
from django.urls import reverse
from django.db import IntegrityError
from django.contrib.auth import authenticate, login, logout
from django.core.exceptions import ObjectDoesNotExist

from .models import User, Blocked

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
            return redirect(reverse("user"))
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
        return redirect(reverse("user"))
    else:  
        return render(request, "forest/register.html")


def user_view(request):
    if request.user.is_authenticated:
        if request.method == 'POST':
            page_name = request.POST['title']
            page_url = request.POST['pageURL']
            #Check if page is in banned list
            banned_list = Blocked.objects.all()

            for banned_page in banned_list:
                if str(banned_page) in page_url:
                    return render(request, 'forest/user.html', {
                        "error": "This page is banned!"
                    })

            #TODO: Add website to the database

            return HttpResponse("Add to the database")
        else:
            return render(request, "forest/user.html")
    else:
        return redirect(reverse("login"))