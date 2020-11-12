from datetime import datetime as dt

from django.shortcuts import render, redirect
from django.http import HttpResponse

# render2pdf
from Senso_facturation.utils import render_to_pdf

# github webhook
import git
from django.views.decorators.csrf import csrf_exempt

from .models import *
from .forms import *

# Create your views here.

# webhook Github
@csrf_exempt
def update(request):
    if request.method == "POST":
        '''
        pass the path of the diectory where your project will be 
        stored on PythonAnywhere in the git.Repo() as parameter.
        Here the name of my directory is "test.pythonanywhere.com"
        '''
        repo = git.Repo("test.pythonanywhere.com/") 
        origin = repo.remotes.origin

        origin.pull()

        return HttpResponse("Updated code on PythonAnywhere")
    else:
        return HttpResponse("Couldn't update the code on PythonAnywhere")

def index(request):
    template_name = 'webpages/index.html'

    context = {

    }

    return render(request, template_name, context)

def test(request):
    template_name = 'webpages/test.html'

    context = {
        'name': 'Nathalie Guillaume',
        'date': '2020-11-12'
    }
    pdf = render_to_pdf(template_name, context)

    return HttpResponse(pdf, content_type = 'application/pdf')
