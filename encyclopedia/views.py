import random
# import markdown2
# Unable to import markdown2
from django.shortcuts import render, redirect

from . import util
from .forms import NewPage, EditPage


def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })

def entry(request, title):
    # Get the entry from files
    entry = util.get_entry(title)
    print(entry)
    # If no entry exists, return error
    if entry == None:
        print("Does not exist")
        error = True
        # Render with error
        return render(request, "encyclopedia/entry.html", {
            'title': title,
            "error": error
        })
    # Render with entry
    return render(request, "encyclopedia/entry.html", {
        'title': title,
        "entry": entry
    })

def search(request):
    # Get query params
    q = request.GET.get('q')
    # If no query, redirect
    if not q:
        return redirect('index')

    # Try and get exact entry
    get = util.get_entry(q)

    # If entry exists, redirect
    if get:
        return redirect('entry', q)

    # else find substring matches
    else:
        # List all entries
        entries = util.list_entries()
        listEntries = []

        # Loop through entries and find matches
        for e in entries:
            if q.lower() in e.lower():
                listEntries.append(e)

        # Return results
        return render(request, "encyclopedia/results.html", {
            'query': q,
            'results': listEntries
        })

def new(request):
    # if POST request
    if request.method == "POST":
        # Get form data
        form = NewPage(request.POST)
        if form.is_valid():
            # clean data
            title = form.cleaned_data["title"]
            content = form.cleaned_data["content"]

            # if entry exists, return error
            if util.get_entry(title):
                return render(request, "encyclopedia/new.html", {
                    'form': form,
                    'error_msg': 'Title Already exists'
                })

            # save entry
            try:
                util.save_entry(title, content)
            except:
                print("Unable to save entry")

            # redirect to new entry
            return redirect('entry', title)
    else:
        # Get blank form
        form = NewPage()
        # return template
        return render(request, 'encyclopedia/new.html', {
            'form': form
        })

def random_entry(request):
    # get list of entries
    entry = util.list_entries()
    # get random entry
    page = random.choice(entry)
    print(page)
    # redirect to random entry
    return redirect('entry', page)

def edit(request, title):
    # get entry
    entry = util.get_entry(title)
    # if doesnt exist, redirect to home
    if entry == None:
        return redirect('index')
    
    # if request is POST
    if request.method == "POST":
        # get form data
        form = EditPage(request.POST)
        if form.is_valid():
            # clean data
            content = form.cleaned_data["content"]
            # update entry
            try:
                util.save_entry(title, content)
            except:
                print("Unable to update")
                # redirect to entry
            return redirect('entry', title)
    else:
        # get blank form
        form = EditPage()
        # return template with form and entry data
        return render(request, "encyclopedia/edit.html", {
            'title': title,
            'form': form,
            'entry': entry
        })
    
