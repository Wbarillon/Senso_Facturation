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
        """
        pass the path of the diectory where your project will be
        stored on PythonAnywhere in the git.Repo() as parameter.
        Here the name of my directory is "test.pythonanywhere.com"
        """
        repo = git.Repo("test.pythonanywhere.com/")
        origin = repo.remotes.origin

        origin.pull()

        return HttpResponse("Updated code on PythonAnywhere")
    else:
        return HttpResponse("Couldn't update the code on PythonAnywhere")


def index(request):
    template_name = "webpages/index.html"

    context = {}

    total = 0
    numFacture = "10000"
    facture = Facture.objects.filter(id_facture=numFacture)
    nbJours = facture.nombre_jours
    servicesCommandes = Service_Produit_Commande.objects.filter(id_facture=numFacture)
    for serviceCommande in servicesCommandes:
        quantite = serviceCommande.quantite
        totalHt = serviceCommande.prix_total_ht - serviceCommande.remise
        total += totalHt
        totalTaxes = 0
        serviceProduit = serviceCommande.service_produit
        idServiceProduit = serviceProduit.id
        taxesService = Taxe_Service_Produit.objects.filter(
            service_produit__id_service_produit=idServiceProduit
        )
        for taxe in taxesService:
            if taxe.type_taxe == "Taux_Sans_Mini":
                taxeAAjouter = totalHt * taxe.taux / 100
            elif taxe.type_taxe == "Taux_Avec_Mini_Global":
                if (totalHt * taxe.taux / 100) < taxe.mini:
                    taxeAAjouter = taxe.mini
                else:
                    taxeAAjouter = totalHt * taxe.taux / 100
            elif taxe.type_taxe == "Taux_Avec_Mini_Par_Jour":
                if (totalHt * taxe.taux / 100 / nbJours) < taxe.mini:
                    taxeAAjouter = taxe.mini * nbJours
                else:
                    taxeAAjouter = totalHt * taxe.taux / 100
            elif taxe.type_taxe == "Montant_Fixe_Global":
                taxeAAjouter = taxe.montant
            elif taxe.type_taxe == "Montant_Fixe_Par_Jour":
                taxeAAjouter = taxe.montant * nbJours
            elif taxe.type_taxe == "Type_Taxe_De_Sejour":
                taxeAAjouter = 0
                personnesFactures = Personne_Facture.objects.filter(
                    facture__id_facture=numFacture
                )
                nbPersonnes = personnesFactures.length
                nbPersonnesAssujetties = 0
                for personneFacture in personnesFactures:
                    if personneFacture.personne.assujettie_taxe_sejour:
                        nbPersonnesAssujetties += 1
                if nbPersonnesAssujetties > 0:
                    taxeAAjouter = (
                        totalHt * taxe.taux / 100 / nbPersonnes * nbPersonnesAssujetties
                    )

            totalTaxes += taxeAAjouter
        total += totalTaxes

    context = {"Numéro de facture": numFacture, "Total HT": totalHt, "Total": total}

    return render(request, template_name, context)


def test(request):
    template_name = "webpages/test.html"

    context = {"name": "Nathalie Guillaume", "date": "2020-11-12"}
    pdf = render_to_pdf(template_name, context)

    return HttpResponse(pdf, content_type="application/pdf")
