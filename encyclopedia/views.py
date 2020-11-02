import random
from django.shortcuts import render, redirect

from . import util
from .forms import NewPage


def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })

def entry(request, title):
    entry = util.get_entry(title)
    print(entry)
    if entry == None:
        print("Does not exist")
        entry = "Sorry, there was an Error. It seems that this entry does not exist."
    return render(request, "encyclopedia/entry.html", {
        'title': title,
        "entry": entry
    })

def search(request):
    q = request.GET.get('q')
    if not q:
        return redirect('index')

    try:
        get = util.get_entry(q)
    except:
        print("No Entries")

    if get:
        return redirect('entry', q)
    else:
        entries = util.list_entries()
        listEntries = []

        for e in entries:
            if q.lower() in e.lower():
                listEntries.append(e)

        return render(request, "encyclopedia/results.html", {
            'query': q,
            'results': listEntries
        })

def new(request):
    if request.method == "POST":
        form = NewPage(request.POST)
        if form.is_valid():
            title = form.cleaned_data["title"]
            content = form.cleaned_data["content"]
            if util.get_entry(title):
                return render(request, "encyclopedia/new.html", {
                    'form': form,
                    'error_msg': 'Title Already exists'
                })
            try:
                util.save_entry(title, content)
            except:
                print("Unable to save entry")
            return redirect('entry', title)
    else:
        form = NewPage()
        return render(request, 'encyclopedia/new.html', {
            'form': form
        })

def random_entry(request):
    entry = util.list_entries()
    page = random.choice(entry)
    print(page)
    return redirect('entry', page)
