from django.shortcuts import render, redirect, HttpResponse
from django.urls import reverse
from django.db import IntegrityError
from django.contrib.auth import authenticate, login, logout
from django.core.exceptions import ObjectDoesNotExist

from .models import User, Blocked, Page

def remove_sessions(request):
    all_sessions = ['error', 'success']

    for session in all_sessions:
        if session in request.session:
            del request.session[session]


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


def add_page(request):
    #TODO check the length of page name and url
    if request.user.is_authenticated:
        if request.method == 'POST':
            #Clear all sessions
            remove_sessions(request)
            
            page_name = request.POST['title']
            page_url = request.POST['pageURL']

            #Check if page is in banned list
            banned_list = Blocked.objects.all()
            for banned_page in banned_list:
                if str(banned_page) in page_url:
                    request.session['error'] = f"Unfortunately <b>{page_url}</b> is blocked!"
                    return redirect(reverse("user"))  
            #Saving data to the database
            save_page = Page.objects.create(
                page_owner = request.user,
                page_name = page_name,
                page_url = page_url
            )
            save_page.save()
            #Set success session
            request.session['success'] = f"{page_name} was added to your desktop!"

        return redirect(reverse("user"))    


def user_view(request):
    if request.user.is_authenticated:
        return render(request, "forest/user.html", {
            "all_pages": Page.objects.all().filter(page_owner = request.user)
        })
    else:
        return redirect(reverse("login"))