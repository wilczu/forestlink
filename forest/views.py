import json
from django.http import JsonResponse
from django.shortcuts import render, redirect, HttpResponse
from django.urls import reverse
from django.db import IntegrityError
from django.contrib.auth import authenticate, login, logout
from django.core.exceptions import ObjectDoesNotExist
from django import forms
from fontawesome_5.forms import IconFormField
from django.contrib import messages
from django.utils.datastructures import MultiValueDictKeyError
from django.core.validators import URLValidator
from django.core.exceptions import ValidationError
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator, EmptyPage

from .models import User, Blocked, Page, Color, Report

class icons_dropdown(forms.Form):
    dropdown = IconFormField(label="Choose the icon")


def pagination(request, data_object, results):
    paginator = Paginator(data_object, results)

    try:
        paginator_result = paginator.page(request.GET.get('page', 1))
    except EmptyPage:
        paginator_result = paginator.page(1)

    return paginator_result


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
            messages.warning(request, "Invalid username or password!")
            return render(request, "forest/login.html")
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
            messages.warning(request, "Your passwords must match.")
            return render(request, "forest/register.html")

        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            messages.warning(request, "This username is taken, please use different one")
            return render(request, "forest/register.html")

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
        #Implement pagination to pages
        all_pages = Page.objects.all().filter(page_owner = request.user).order_by('-id')
        pages = pagination(request, all_pages, 20)

        return render(request, "forest/user.html", {
            "all_pages": pages,
            "icons_dropdown": icons_dropdown()
        })
    else:
        return redirect(reverse("login"))


def remove_page(request):
    if request.user.is_authenticated and request.method == "POST":
        #Try to save ID from removeID field
        try:
            pageID = request.POST['removeID']
        except MultiValueDictKeyError:
            messages.warning(request, "Inappropriate HTML format")
            return redirect(reverse("user"))
        #Try to get the page from a database
        try:
            page = Page.objects.get(pk=int(pageID))
        except ObjectDoesNotExist:
            messages.warning(request, "Page not found")
            return redirect(reverse("user"))
        
        #Check if user owns this page
        if request.user == page.page_owner:
            #Remove color and page from the datbaase
            page.page_color.delete()
            page.delete()
            messages.success(request, "Page was removed successfully")
            return redirect(reverse("user"))
        else:
            messages.warning(request, "You can only edit your pages!")
            return redirect(reverse("user"))
    else:
        return redirect(reverse("user"))


def report_view(request):
    if request.user.is_authenticated:
        #Implement pagination to reports
        all_reports = Report.objects.all().filter(reported=request.user).order_by('-id')
        reports = pagination(request, all_reports, 20)

        return render(request, 'forest/report.html', {
            "all_reports": reports
        })
    else:
        return redirect(reverse("login"))


def process_report(request):
    if request.method == "POST" and request.user.is_authenticated:
        block = request.POST['reportPage']
        error = False

        #Check if this is an actual URL of the page
        validate = URLValidator()
        try:
            validate(block)
        except ValidationError as exception:
            error = True
            messages.warning(request, "Please provide correct URL")

        #check the length of block page
        if len(block) >=2001:
            error = True
            message.warning(request, "Your URL is too long")

        #Check if the website is in blocked list
        banned_list = Blocked.objects.all()
        for banned_page in banned_list:
            if str(banned_page) in block:
                error = True
                messages.warning(request, f"Unfortunately {block} is already blocked!")
                break
    
        #Check if the website is in report list
        report_list = Report.objects.all()
        for report_item in report_list:
            if str(report_item.page) in block:
                error = True
                messages.warning(request, f"Page {block} was already reported")
                break

        if error:
            return redirect(reverse("report"))
        else:
            #Add this URL to the Report table
            save_report = Report.objects.create(
                reported = request.user,
                page = block,
            )
            save_report.save()
            #Return to the report page
            messages.success(request, f"{block} was reported!")
            return reverse(redirect("report"))
    else:
        return reverse(redirect("report"))


def settings_view(request):
    if request.user.is_authenticated:
        return render(request, "forest/settings.html")
    else:
        return render(reverse("login"))


@login_required()
def page_data(request, page_id):
    #Check if request method is correct
    if request.method !="GET":
        return JsonResponse({"error": "Incorrect request method!"}, status=400)

    #Try to get the page from the database
    try:
        get_page = Page.objects.get(pk=int(page_id))
    except ObjectDoesNotExist:
        return JsonResponse({"error": "Page not found!"}, status=404)

    #Check if user is an author of the page
    if request.user == get_page.page_owner:
        return JsonResponse({
            "name": get_page.page_name,
            "url": get_page.page_url,
            "BGcolor": get_page.page_color.background_color,
            "TxTcolor": get_page.page_color.text_color,
        }, status=201)

    else:
        return JsonResponse({"error" : "You can only get data about your pages!"}, status=401)