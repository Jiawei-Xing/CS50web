from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
from .models import User, Project
import json
from bs4 import BeautifulSoup as BS


def index(request):
    return render(request, "webpage/index.html")


def instruction(request):
    return render(request, "webpage/instruction.html")
        

# user-related login, logout, and register are adpoted from previous projects    
def login_view(request):
    if request.method == "POST":

        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "webpage/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "webpage/login.html")


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))


def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "webpage/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "webpage/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "webpage/register.html")
        
        
@login_required
def create(request):
    if request.method == "POST":
    
        # edit
        if 'content' in request.POST:
            soup = BS(request.POST['content'])
            tags = [str(tag) for tag in soup.find_all()]
            old_html = ''
            count=0
            for tag in tags:
                if tag[:4] == "<h1>":
                    count += 1
                    value = tag[4:-5]
                    old_html += f"[{count}]Heading1:<br><textarea name='h1-{count}' id='input{count}' oninput='H1({count})';>{value}</textarea><br>"
                elif tag[:4] == "<h2>":
                    count += 1
                    value = tag[4:-5]
                    old_html += f"[{count}]Heading2:<br><textarea name='h2-{count}' id='input{count}' oninput='H2({count})';>{value}</textarea><br>"
                elif tag[:4] == "<h3>":
                    count += 1
                    value = tag[4:-5]
                    old_html += f"[{count}]Heading3:<br><textarea name='h3-{count}' id='input{count}' oninput='H3({count})'>{value}</textarea><br>"
                elif tag[:3] == "<p>":
                    count += 1
                    value = tag[3:-4]
                    old_html += f"[{count}]Text:<br><textarea name='text-{count}' id='input{count}' oninput='Text({count})'>{value}</textarea><br>"
                elif tag[:4] == "<li>":
                    count += 1
                    value = tag[4:-5]
                    old_html += f"[{count}]Bullet Point:<br><textarea name='ul-{count}' id='input{count}' oninput='Ul({count})'>{value}</textarea><br>"
                elif tag[:7] == "<title>":
                    title = tag[7:-8]

            return render(request, "webpage/create.html", {
                "old_html": old_html, "count": count, "title": title
            })
        
        # create new
        html = f"<!DOCTYPE html>\n<html lang='en'>\n<head><title>{request.POST['title']}</title></head>\n<body>"
        i=0
        while True:
            i += 1
            if f"h1-{i}" in request.POST:
                html += "<h1>" + str(request.POST[f"h1-{i}"]) + "</h1>\n"
            elif f"h2-{i}" in request.POST:
                html += "<h2>" + str(request.POST[f"h2-{i}"]) + "</h2>\n"
            elif f"h3-{i}" in request.POST:
                html += "<h3>" + str(request.POST[f"h3-{i}"]) + "</h3>\n"
            elif f"text-{i}" in request.POST:
                html += "<p>" + str(request.POST[f"text-{i}"]) + "</p>\n"
            elif f"ul-{i}" in request.POST:
                html += "<ul><li>" +str(request.POST[f"ul-{i}"]) + "</li></ul>\n"
            else:
                html += "</body>"
                break  
        if request.POST['title'] == '':
            return HttpResponse("Must provide a title!")
        new = Project.objects.create(creator = request.user, title = request.POST['title'], content = html)
        new.save()     
        return HttpResponseRedirect(reverse("profile"))
    else:        
        return render(request, "webpage/create.html", {
            "old_html": '', "count": 0, "title": ''
        })
        
        
@login_required
def profile(request):

    # delete
    if request.method == "POST":
        Project.objects.get(id = request.POST['del']).delete()
        return HttpResponseRedirect(reverse("profile"))
        
    # show list
    user = User.objects.get(username = request.user)
    projects = Project.objects.filter(creator = user)
    return render(request, "webpage/profile.html", {
        "projects": projects
    })
    
    
@login_required
def project(request, projectid):
    project = Project.objects.get(id = projectid)
    
    # ensure own projects
    if project.creator != request.user:
        return HttpResponse("No access to this project!")
    return render(request, "webpage/project.html", {
        "project": project    
    })
    
