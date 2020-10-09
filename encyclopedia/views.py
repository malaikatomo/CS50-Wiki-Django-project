from django.shortcuts import redirect, render 
from django import forms
from random import randint

from . import util

from markdown2 import Markdown
#use the Markdown() function
markdowner = Markdown()


class NewPageForm(forms.Form):
    name = forms.CharField(label="Name of Page")
    content = forms.CharField(label="Content of page", widget =forms.Textarea())

#Index 
def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })

#load and display the .md file pages 
def title(request, title):

    #variable to see if there is a page with this title
    content = util.get_entry(title)

    #check if content is true 
    if content:
        paragraph = markdowner.convert(content)

        return render(request, "encyclopedia/TITLE.html", {
        "title": title.capitalize(),
        "entry": paragraph
    })
    #no page exist
    else:
        return render(request, "encyclopedia/Error.html",{
            "msg": "No page found"
        })
        return

#Search done
def search(request):
    search = request.GET.get("q")

    #list of all entries
    all_entries = util.list_entries()

    if search in all_entries:
        return redirect(f"/wiki/{search}")
    
    #test for substrings
    result = [i for i in all_entries if search.capitalize() in i.capitalize()]
    if len(result) ==0:
        return render(request, "encyclopedia/Error.html",{
            "msg": "No matches found"
        })
    else:
        return render(request, "encyclopedia/Search.html",{
            "entries": result,
            "search": search
        })

#New page done
def newPage(request):
    if request.method == "POST":
        entries = util.list_entries()
        #get user submitted data
        form = NewPageForm(request.POST)
        if form.is_valid():
            name = form.cleaned_data["name"]
            content = form.cleaned_data["content"]
            if name in entries:
                #error
                return render(request, "encyclopedia/Error.html",{
                    "msg": "Page already exists"
                })
            paragraph = f'# {name}\n\n {content}'
            util.save_entry(name, paragraph)
            return title(request, name)
            

    return render(request, "encyclopedia/Create.html", {
        "form": NewPageForm()
    })

#Random Page 
def random(request):
    all_entries = util.list_entries()
    randomNum = randint(0,len(all_entries)-1)
    random_entry = all_entries[randomNum]
    return redirect(f"/wiki/{random_entry}")

#edit Page  
def editPage(request,title):

    if request.method == "POST":
        #get the content from edited page
        new_content = request.POST['content']
        #Save it 
        util.save_entry(title,new_content)
        return redirect(f"/wiki/{title}")
    else:
        #Get the page with the original context
        return render(request, "encyclopedia/editPage.html", {
            'title': title,
            'edit': util.get_entry(title)
        })
    
