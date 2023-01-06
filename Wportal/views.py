import imp
from multiprocessing.dummy import current_process
from unicodedata import name
from django.db import IntegrityError
from django.shortcuts import render, redirect
from django.http import HttpResponseRedirect, JsonResponse
from django.urls import reverse
from .models import User, Teacher, Student, Note, Event
from django.contrib.auth import authenticate, login, logout
import json
from django.views.decorators.csrf import csrf_exempt
import smtplib
from .forms import NoteForm
from datetime import *
temp = date.today()
year = int(temp.strftime("%Y"))
mon = int(temp.strftime("%m"))
day = int(temp.strftime("%d"))
first = date(year, 1, 1)
second = date(year, 6, 1)
current = date(year, mon, day)

if(current >= first and current <= second):
    term = "FirstTerm"
else:
    term = "SecondTerm"
print(term)


def index(request):
    return render(request, "index.html")


def login_view(request):
    if request.method == "POST":
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password,)
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "login.html")


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))


def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        category = request.POST["user_type"]

        if password != confirmation:
            return render(request, "register.html", {
                "message": "Passwords must match."
            })
        try:
            user = User.objects.create_user(
                username, email, password, user_type=category)
            user.save()
        except IntegrityError:
            return render(request, "register.html", {
                "message": "Username already taken."
            })
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "register.html")


def upload_file(request):
    if request.method == "POST":
        user = request.user.username
        standard = request.POST['standard']
        subject = request.POST['subject']
        unit = request.POST['unit']
        title = request.POST['title']
        filterStudent = Student.objects.filter(standard=standard)
        form = NoteForm(request.POST, request.FILES)

        if form.is_valid():
            form.save()
            for i in filterStudent:
                server = smtplib.SMTP_SSL("smtp.gmail.com", 465)
                server.login("ashokmithra02072003@gmail.com", "ashok2003*")
                server.sendmail("ashokmithra02072003@gmail.com",
                                i.user.email, user+" posted " + title + " for subject "+subject + " and unit "+unit)
                server.quit()
            return redirect('index')
    else:
        form = NoteForm()
    return render(request, 'createNote.html', {
        'form': form
    })


def profile(request, id):
    users = User.objects.get(id=id)
    try:
        check = Teacher.objects.get(user=users)
        c = True
    except Teacher.DoesNotExist:
        c = False
    try:
        check2 = Student.objects.get(user=users)
        c2 = True
    except Student.DoesNotExist:
        c2 = False
    if(users.user_type == "Teacher"):
        if(c):
            return render(request, "createProfile.html", {
                "profile": check
            })
        else:
            return render(request, "createProfile.html")
    else:
        if(c2):
            return render(request, "createProfile.html", {
                "profile": check2
            })
        else:
            return render(request, "createProfile.html")


def filters(request):
    if request.method == "POST":
        sub = request.POST['subject']
        title = request.POST["title"]
        if(request.user.user_type == "Student"):
            user = request.user
            gets = Student.objects.get(user=user)
            print(gets.standard)
            fil = Note.objects.filter(
                subject=sub, title=title, standard=gets.standard, term=term)
        else:
            standard = request.POST['standard']
            fil = Note.objects.filter(
                subject=sub, title=title, standard=standard, term=term)
        return render(request, "allNotes.html", {
            'allnote': fil,
        })
    else:
        return render(request, "filter.html")


@csrf_exempt
def searchs(request):
    if request.method == "POST":
        details = json.loads(request.body)
        if(request.user.user_type == "Teacher"):
            s1 = details["sta"]
        else:
            temp = Student.objects.get(user=request.user)
            s1 = temp.standard
        s2 = details["sub"].title()
        types = details["type"].title()
        try:
            store = Note.objects.filter(
                standard=s1, subject=s2, title=types, term=term)
            flag = True
            return JsonResponse({'allnotes': [p.serialize() for p in store], 'flag': flag})
        except Note.DoesNotExist:
            flag = False
            return JsonResponse({'flag': flag})
    else:
        return JsonResponse({"post": "Post method required"})


def upload_event(request):
    if request.method == "POST":
        temp = Event(
            title=request.POST["title"],
            eligibility=request.POST["eligibility"],
            edob=request.POST["edob"],
            rsdob=request.POST["rsdob"],
            rddob=request.POST["rddob"],
            ed=request.POST["ed"],
            link=request.POST["link"]
        )
        temp.save()
        return redirect("index")
    else:
        return render(request, "createEvent.html")


def event(request):
    filt = Event.objects.all()
    return render(request, "allEvent.html", {
        "allevent": filt
    })
