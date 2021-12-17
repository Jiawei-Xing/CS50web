from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse

from random import randint
import markdown2

from . import util


def index(request):
    if request.method == "POST":
        if util.get_entry(request.POST['q']):
            return HttpResponseRedirect(reverse('index') + 'wiki/' + request.POST['q'])
        else:
            entries = []
            for each in util.list_entries():
                if request.POST['q'] in each:
                    entries.append(each)
            return render(request, "encyclopedia/result.html", {
            "entries": entries
        })
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })


def entry(request, title):
    entry = util.get_entry(title)
    if entry:
        return render(request, "encyclopedia/entry.html", {
        "title": title, "entry": markdown2.markdown(entry)
    })
    else:
        return HttpResponse(f"Error: {title} is not found")
        
        
def create(request):
    if request.method == "POST":
        title = request.POST['title']
        content = request.POST['content']
        if title in util.list_entries():
            return HttpResponse(f"Error: {title} already exists")
        else:
            util.save_entry(title, content)
            return HttpResponseRedirect(reverse('index') + 'wiki/' + title)
    return render(request, "encyclopedia/create.html")


def edit(request, title):
    if request.method == "POST":
        util.save_entry(title, request.POST['content'])
        return HttpResponseRedirect(reverse('index') + 'wiki/' + title)
    return render(request, "encyclopedia/edit.html", {
    "title": title, "content": util.get_entry(title)
})


def random(request):
    title = util.list_entries()[randint(0, len(util.list_entries()) - 1)]
    return HttpResponseRedirect(reverse('index') + 'wiki/' + title)


