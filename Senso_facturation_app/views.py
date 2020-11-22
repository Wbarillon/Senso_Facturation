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


def CalculerTotaux(numFacture):
    total = 0
    totalHt = 0
    totalTaxes = 0
    numFacture = "10000"
    factures = Facture.objects.filter(numero_facture=numFacture)
    facture = factures[0]
    nbJours = facture.nombre_jours
    servicesCommandes = Service_Produit_Commande.objects.filter(facture_id=facture.id)
    for serviceCommande in servicesCommandes:
        quantite = serviceCommande.quantite
        totalHtService = serviceCommande.prix_total_ht - serviceCommande.remise
        totalHt += totalHtService
        serviceProduit = serviceCommande.service_produit
        idServiceProduit = serviceProduit.id
        for taxe in serviceCommande.service_produit.taxes.all():
            if taxe.type_taxe == "Taux_Sans_Mini":
                taxeAAjouter = totalHtService * taxe.taux / 100
            elif taxe.type_taxe == "Taux_Avec_Mini_Global":
                if (totalHtService * taxe.taux / 100) < taxe.mini:
                    taxeAAjouter = taxe.mini
                else:
                    taxeAAjouter = totalHtService * taxe.taux / 100
            elif taxe.type_taxe == "Taux_Avec_Mini_Par_Jour":
                if (totalHtService * taxe.taux / 100 / nbJours) < taxe.mini:
                    taxeAAjouter = taxe.mini * nbJours
                else:
                    taxeAAjouter = totalHtService * taxe.taux / 100
            elif taxe.type_taxe == "Montant_Fixe_Global":
                taxeAAjouter = taxe.montant_fixe
            elif taxe.type_taxe == "Montant_Fixe_Par_Jour":
                taxeAAjouter = taxe.montant_fixe * nbJours
            elif taxe.type_taxe == "Type_Taxe_De_Sejour":
                taxeAAjouter = 0

                nbPersonnes = len(facture.personnes.all())
                nbPersonnesAssujetties = 0
                for personne in facture.personnes.all():
                    if personne.assujettie_taxe_sejour:
                        nbPersonnesAssujetties += 1
                if nbPersonnesAssujetties > 0:
                    taxeAAjouter = (
                        totalHtService
                        * taxe.taux
                        / 100
                        / nbPersonnes
                        * nbPersonnesAssujetties
                    )

            totalTaxes += taxeAAjouter

    total = totalHt + totalTaxes

    resultat = {
        "numFacture": numFacture,
        "totalHt": totalHt,
        "totalTaxes": totalTaxes,
        "total": total,
    }

    return resultat


def index(request):
    template_name = "webpages/index.html"

    context = CalculerTotaux("10000")

    """
    context = {
        "numFacture": numFacture,
        "totalHt": totalHt,
        "totalTaxes": totalTaxes,
        "total": total,
    }
    """

    return render(request, template_name, context)


def test(request):
    template_name = "webpages/test.html"

    context = {"name": "Nathalie Guillaume", "date": "2020-11-12"}
    pdf = render_to_pdf(template_name, context)

    return HttpResponse(pdf, content_type="application/pdf")
