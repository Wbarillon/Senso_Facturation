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


def CalculerTotaux(facture):
    total = 0
    totalHt = 0
    totalTaxes = 0
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
                nbPersonnes = len(facture.personnes.all())
                if nbPersonnes == 0 or nbJours == 0:
                    taxeAAjouter = 0
                else:
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
                        if (taxeAAjouter / nbJours) < taxe.mini:
                            taxeAAjouter = taxe.mini * nbJours

            totalTaxes += taxeAAjouter

    total = totalHt + totalTaxes

    resultat = {
        "numFacture": facture.numero_facture,
        "totalHt": round(totalHt, 2),
        "totalTaxes": round(totalTaxes, 2),
        "total": round(total, 2),
    }

    return resultat


def index(request):
    template_name = "webpages/index.html"

    # le else avec numero_facture = 0 inutile, mais j'imagine que c'est comme ça que tu voulais
    # gérer le cas où la première facture n'a pas encore été générée
    if request.POST:
        emetteur_facture = request.POST.get("emetteur_facture")
        if emetteur_facture == "Asso":
            numero_facture = str(
                Dernier_Numero_Facture.objects.all()[0].facture_asso + 1
            )
        elif emetteur_facture == "Senso":
            numero_facture = str(
                Dernier_Numero_Facture.objects.all()[0].facture_senso + 1
            )
        else:
            numero_facture = "0"
    else:
        numero_facture = "0"

    form = AddFacture(
        request.POST or None,
        reponse=request.POST.get("question"),
        numero_facture=numero_facture,
    )

    fields = [
        "emetteur_facture",
        "client",
        "numero_facture",
        "numero_commande",
        "date_arrivee",
        "date_depart",
        "nb_jours",
        "montant_arrhes",
        "modes_paiement_arrhes",
        "date_paiement_arrhes",
        "montant_solde",
        "modes_paiement_solde",
        "date_paiement_solde",
        "remarques",
        "question",
    ]

    context = {"form": form}

    """
        for field in fields:
            if request.POST.get(field) != None:
                request.session.update({field: request.POST.get(field)})
            else:
                pass

        data = {key: value for key, value in request.session.items() if key in fields}
    """

    """
    factures = Facture.objects.all()
    facture = factures[0]
    context = CalculerTotaux(facture)

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
