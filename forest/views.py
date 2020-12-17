from django.shortcuts import render, redirect, HttpResponse
from django.urls import reverse
from django.db import IntegrityError
from django.contrib.auth import authenticate, login, logout
from django.core.exceptions import ObjectDoesNotExist
from django import forms
from fontawesome_5.forms import IconFormField
from django.contrib import messages

from .models import User, Blocked, Page, Color

class icons_dropdown(forms.Form):
    dropdown = IconFormField(label="Choose the icon")


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
    if request.user.is_authenticated:
        if request.method == 'POST':
            
            page_name = request.POST['title']
            page_url = request.POST['pageURL']
            page_background = request.POST['bgColor']
            text_color = request.POST['textColor']
            page_icon = request.POST['dropdown']

            #Check if page name, icon and url have correct length
            if len(page_name) <= 0 or len(page_name) > 120:
                messages.warning(request, "Your page name is too short or too long")
                return redirect(reverse("user"))
            if len(page_url) <= 0 or len(page_url) > 2000:
                messages.warning(request, "Your page url is too short or too long")
                return redirect(reverse("user"))
            if len(page_icon) <=1:
                messages.warning(request, "Please specify the Icon for your page")
                return redirect(reverse("user"))

            #Check if page is in banned list
            banned_list = Blocked.objects.all()
            for banned_page in banned_list:
                if str(banned_page) in page_url:
                    messages.warning(request, f"Unfortunately {page_url} is blocked!")
                    return redirect(reverse("user"))  

            #Saving colors to the database
            save_colors = Color.objects.create(
                background_color = page_background,
                text_color = text_color
            )
            save_colors.save()

            #Saving data to the database
            save_page = Page.objects.create(
                page_owner = request.user,
                page_name = page_name,
                page_url = page_url,
                page_color = save_colors,
                page_icon = page_icon
            )
            save_page.save()

            #Set success session
            messages.success(request, f"{page_name} was added to your desktop!")

        return redirect(reverse("user"))    


def user_view(request):
    if request.user.is_authenticated:
        return render(request, "forest/user.html", {
            "all_pages": Page.objects.all().filter(page_owner = request.user),
            "icons_dropdown": icons_dropdown()
        })
    else:
        return redirect(reverse("login"))