from django.shortcuts import render, redirect
from django.http import HttpResponse
from django import forms

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

            for entry in entries:
                if title.lower() == entry.lower():
                    return redirect('index')


            print(title)
        return render(request, "encyclopedia/newpage.html", {
        "form": NewPageForm()
        })

    




class NewPageForm(forms.Form):
    newpagetitle = forms.CharField(widget = forms.TextInput(attrs={'class': 'form-control', 'id': 'titleinput', 'style': 'max-width: 300px;'}), label="Page Title")
    newpagecontent = forms.CharField(widget = forms.Textarea(attrs={'class': 'form-control'}), label="Page Content")
