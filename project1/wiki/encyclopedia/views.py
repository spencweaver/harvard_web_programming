from django import forms
from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse

from . import util

import markdown2

import random


class ArticleDoesNotExist(Exception):
    pass


class NewArticle(forms.Form):
    title = forms.CharField(label="Title")
    body = forms.CharField(label="Body", widget=forms.Textarea)


def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })


def title(request, title):
    try:
        return render(request, "encyclopedia/title.html", {
            "title": markdown2.markdown(util.get_entry(title)),
            "edit": util.get_entry(title),
            "edit_title": title
        })
    except ArticleDoesNotExist:
        return render(request, "encyclopedia/error.html")


def search(request):
    query = request.GET.get('q')
    list = []
    if util.get_entry(query) is None:
        # check for partial search matches
        for i in util.list_entries():
            if i.casefold().startswith(query):
                list.append(i)
        return render(request, "encyclopedia/index.html", {
                "entries": list
            })
    return HttpResponseRedirect(reverse('title', args=[query]))


def newpage(request):
    if request.method == "POST":
        form = NewArticle(request.POST)
        if form.is_valid():
            title = form.cleaned_data["title"]
            body = form.cleaned_data["body"]
            util.save_entry(title, body)
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "encyclopedia/newpage.html", {
                "article": form
            })
    return render(request, "encyclopedia/newpage.html", {
        "article": NewArticle()
    })


def randoma(request):
    entries = util.list_entries()
    n = random.randint(0, len(entries)-1)
    return HttpResponseRedirect(reverse('title', args=[entries[n]]))


def edit(request):
    if request.method == "POST":
        form = NewArticle(request.POST)
        if form.is_valid():
            title = form.cleaned_data["title"]
            body = form.cleaned_data["body"]
            util.save_entry(title, body)
            return HttpResponseRedirect(reverse("index"))

    # Collect information to make the form editable
    edit_body = request.GET.get('edit_body')
    edit_title = request.GET.get('edit_title')

    # Create an object to send to edit form
    object = {"title": edit_title, "body": edit_body}

    return render(request, "encyclopedia/edit.html", {
        "article": NewArticle(object)
    })
