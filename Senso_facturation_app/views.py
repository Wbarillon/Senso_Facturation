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
    # Utilisation d'un modelformset comme sur la vidéo https://www.youtube.com/watch?v=JIvJL1HizP4
    # Implique que les modèles soient clean
    template_name = 'webpages/index.html'

    fields = ['service', 'paiement']

    context = {

    }

    if request.method == 'POST':
        ServiceCommandeFormset = modelformset_factory(Service_Produit_Commande)

    #form = AddService(request.POST or None)
    '''
    formset_extra = 3

    AddServiceFormSet = formset_factory(AddService, extra = formset_extra, can_delete = False)

    
    formset = AddServiceFormSet(initial = [
        {
            'service': '0bcda',
            'paiement': 'a'
        },
        {
            'service': 'fdjsqfmq',
            'paiement': 'fsdf'
        }
    ])
    
    
    #initial = [{'service': 'sauna', 'paiement': 'espèce'}, {'service': 'goûter', 'paiement': 'bisous'}]
    #initial.append({'service': 'youpii'})
    
    
    for key in list(request.session.keys()):
        del request.session[key]
    

    context = {
        'formset': AddServiceFormSet
    }



    if request.POST.get('oui'):

        formset_extra += 1

        # Enregistrer les informations de request.POST dans request.session, pour pouvoir les rappeler
        # au besoin lors de l'ajout de formulaire "extra".
        for i in range(formset_extra):
            for field in fields:
                if request.POST.get('form'+'-'+str(i)+'-'+field) != None:
                    request.session.update({
                        'form'+'-'+str(i)+'-'+field: request.POST.get('form'+'-'+str(i)+'-'+field)
                    })
                else:
                    pass

        data = {key: value for key, value in request.session.items()}
        print(data)

        initial = []
        for i in range(formset_extra):
            for field in fields:
                if 'form'+'-'+str(i)+'-'+field in data:
                    print('form'+'-'+str(i)+'-'+field)
        
        AddServiceFormSet = formset_factory(AddService, extra = formset_extra)
        # Récupérer les données de data et les attribuer "à la bonne ligne"
        # Dans data, il y a plusieurs dictionnaire, formset_extra de dictionnaire pour être exacte
        # et les clés de dictionnaire sont déclarés plus haut dans fields
        # Objectif : créer une boucle qui déclare formset_extra dictionnaires avec les champs de fields
        formset = AddServiceFormSet(initial = initial)

        context.update({'formset': formset})

    
    if request.POST.get('oui'):

        for field in fields:
            if request.POST.get(field) != None:
                request.session.update({field: request.POST.get(field)})
            else:
                pass

        formset_extra

        #print(request.POST)
        
        for field in fields:
            #print(field)
            #print(request.POST)
            if field in request.POST:
                print(request.POST)
            #if field in request.POST.get(field):
            #    request.session.update({field: request.POST.get(field)})
            #else:
            #    pass
        
    

        print(request.session.items())

        formset_extra += 1
        print(formset_extra)

        AddServiceFormSet = formset_factory(AddService, extra = formset_extra)
        formset = AddServiceFormSet(request.POST or None)
        context.update({'formset': AddServiceFormSet})
    '''

    return render(request, template_name, context)

def test(request):
    template_name = 'webpages/test.html'

    context = {
        'name': 'Nathalie Guillaume',
        'date': '2020-11-12'
    }
    pdf = render_to_pdf(template_name, context)

    return HttpResponse(pdf, content_type = 'application/pdf')

def ajout_culture(request):
    template_name = 'forms/one_step_form.html'

    form = AddCulture(request.POST or None, reponse = request.POST.get('question'))

    models = [Culture, PhaseCulture]

    fields = ['type_contenant', 'nom', 'phase', 'phase_date']

    context = {
        'form': form
    }

    if (request.POST.get('question') == 'Non') and (request.POST.get(fields[-1]) == ''):
        pass

    elif (request.POST.get('question') == 'Non') or ((request.POST.get('question') == 'Oui') and (request.POST.get(fields[-1]) != None)):

        for field in fields:
            if request.POST.get(field) != None:
                request.session.update({field: request.POST.get(field)})
            else:
                pass

        if request.POST.get('question') == 'Oui':
            request.session.update({'reponse': 'Oui'})

        data = {key: value for key, value in request.session.items() if key in fields}

        labels = []
        
        for model in models:
            for field_name in fields:
                try:
                    labels.append(getattr(model, field_name).field.verbose_name)
                except AttributeError:
                    pass

        data_front = {label: value for label, value in zip(labels, data.values())}

        context.update({'data_front': data_front})

    elif request.POST.get('recommencer') != None:

        # Since we restart the form, we better have to clean request.session before

        if 'reponse' in dict(request.session.items()):
            del request.session['reponse']

        for field in fields:
            try:
                del request.session[field]
            except KeyError:
                pass

        return redirect('ajout_culture')

    elif request.POST.get('sauvegarder') != None:

        data = {key: value for key, value in request.session.items() if key in fields}

        data_back = {}

        for key, value in data.items():
            if key.endswith('date') and (value != ''):
                data_back.update({key: dt.strptime(value, '%d-%m-%Y').strftime('%Y-%m-%d')})
            elif (key.endswith('date')) and (value == ''):
                data_back.update({key: None})
            else:
                data_back.update({key: value})

        instance = Culture()

        for key, value in data_back.items():
            setattr(instance, key, value)
        instance.save()

        if ('reponse' in dict(request.session.items())) and (request.session['reponse'] == 'Oui'):

            data_back.update({'nom_culture': Culture.objects.get(nom = data['nom'])})

            instance = PhaseCulture()

            for key, value in data_back.items():
                setattr(instance, key, value)
            instance.save()

        # Once data are saved, we can clean request.session

        for field in fields:
            try:
                del request.session[field]
            except KeyError:
                pass
        
        return redirect('etat_jardin')

    return render(request, template_name, context)