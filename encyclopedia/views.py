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
    matches = []
    for entry in entries:
        # Returning exact match page if there is one
        if term.lower() == entry.lower():
            return redirect('entry', title=term.capitalize())

        # Appending substring matches to a list
        elif term.lower() in entry.lower():
            matches.append(entry)
            


    # Return search page, with term and possibly empty list of partial matches passed in
    return render(request, "encyclopedia/search.html", {
                "term": term,
                "matches": matches
            })

