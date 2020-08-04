from django.shortcuts import render, redirect
from django.http import HttpResponse

from . import util


def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })

def entry(request, title):
    if util.get_entry(title) is None:
        return render(request, "encyclopedia/error.html", {
            "title": title
        })
    else:
        return render(request, "encyclopedia/entry.html", {
            "title": title,
            "entry": util.get_entry(title)
        })

def search(request):
    term = request.POST['q']
    entries = util.list_entries()
    print(term)
    for entry in entries:
        if term.lower() == entry.lower():
            return redirect('entry', title=term)
        else:
            return render(request, "encyclopedia/search.html", {
                "term": term
            })
            # return render(request, "encyclopedia/entry.html", {
            #     "title": entry,
            #     "entry": util.get_entry(entry)
            # })
