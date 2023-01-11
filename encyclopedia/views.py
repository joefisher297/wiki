from django.shortcuts import render, redirect
from django.http import HttpResponse
from django import forms
from django.contrib import messages
import random

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

def newpage(request):

    # Checking to see whether we've just submitted this very form
    if request.method == 'POST':
        # Create a new form object with the data that's just been input 
        form = NewPageForm(request.POST)

        # If the form's good, create new string variables out of the inputs
        if form.is_valid():
            title = form.cleaned_data["newpagetitle"]
            content = form.cleaned_data["newpagecontent"]

            entries = util.list_entries()

            # Check if the entry already exists. If it does, reload the new entry page with an error message. 
            for entry in entries:
                if title.lower() == entry.lower():
                    messages.warning(request,'That page already exists!')
                    return render(request, "encyclopedia/newpage.html", {
                        "form": NewPageForm()
                    })

            # If we've made it this far, save the new entry and redirect us to that page 
            util.save_entry(title, content)
            return redirect('entry', title=title.capitalize())

    
    # If we've been sent here by GET (i.e. clicked "Create New Page" on sidebar) return the page with a fresh form
    return render(request, "encyclopedia/newpage.html", {
    "form": NewPageForm()
    })


def editpage(request, title):

    # If we've just submitted the form on the page
    if request.method == 'POST':
        form = NewPageForm(request.POST)

        if form.is_valid():
            title = form.cleaned_data["newpagetitle"]
            content = form.cleaned_data["newpagecontent"]

            # Save (overwrite) the entry with the given title and send us to that page. 
            util.save_entry(title, content)
            return redirect('entry', title=title.capitalize())

    elif util.get_entry(title) is None:
        return render(request, "encyclopedia/error.html", {
            "title": title
        })

    else:
        content = util.get_entry(title)
        form = NewPageForm(initial= {
            'newpagetitle': title, 
            'newpagecontent': content
        })
        return render(request, "encyclopedia/editpage.html", {
            "title": title,
            "entry": content,
            "form": form
        })  


def randompage(request):
    entries = util.list_entries()
    entry = entries[random.randrange(len(entries))]
    return redirect('entry', title=entry)
    




class NewPageForm(forms.Form):
    newpagetitle = forms.CharField(widget = forms.TextInput(attrs={'class': 'form-control', 'id': 'titleinput', 'style': 'max-width: 300px;'}), label="Page Title")
    newpagecontent = forms.CharField(widget = forms.Textarea(attrs={'class': 'form-control'}), label="Page Content")
  

