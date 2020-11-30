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


def CalculerTotauxFacture(facture):
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


def CalculerTotauxParTva(facture):
    dicoTaxesTva = {}

    cleTaux = "Taux"
    cleTotalHt = "Total HT"
    cleTotalTaxe = "Total Taxe"

    servicesCommandes = Service_Produit_Commande.objects.filter(facture_id=facture.id)
    for serviceCommande in servicesCommandes:
        for taxe in serviceCommande.service_produit.taxes.all():
            if taxe.initiales[0:3].upper() == "TVA":
                if not taxe.nom_taxe in dicoTaxesTva.keys():
                    dicoTaxesTva[taxe.nom_taxe] = {}
                    dicoTaxesTva[taxe.nom_taxe][cleTaux] = taxe.taux
                    dicoTaxesTva[taxe.nom_taxe][cleTotalHt] = 0
                    dicoTaxesTva[taxe.nom_taxe][cleTotalTaxe] = 0

    if len(dicoTaxesTva) == 0:
        return {}

    for serviceCommande in servicesCommandes:
        for taxe in serviceCommande.service_produit.taxes.all():
            if taxe.nom_taxe in dicoTaxesTva.keys():
                dicoTaxesTva[taxe.nom_taxe][cleTotalHt] += (
                    serviceCommande.prix_total_ht - serviceCommande.remise
                )

    for taxeTva in dicoTaxesTva.keys():
        dicoTaxesTva[taxeTva][cleTotalTaxe] = round(
            dicoTaxesTva[taxeTva][cleTotalHt] * dicoTaxesTva[taxeTva][cleTaux] / 100, 2
        )

    return dicoTaxesTva


def index(request):
    template_name = "webpages/index.html"

    fields = [
        "emetteur_facture",
        "client",
        "numero_facture",
        "numero_commande",
        "date_arrivee",
        "date_depart",
        "remarques",
    ]


    if request.POST:
        """
        for field in fields:
            if request.POST.get(field) != None:
                request.session.update({field: request.POST.get(field)})
            else:
                pass
        """
        data = {key: value for key, value in request.POST.items() if key in fields}

        dernierNumeroFacture = Dernier_Numero_Facture.objects.all()[0]
        if data["emetteur_facture"] == "Asso":
            dernierNumeroFacture.facture_asso += 1
            numeroFacture = str(dernierNumeroFacture.facture_asso)
        elif data["emetteur_facture"] == "Senso":
            dernierNumeroFacture.facture_senso += 1
            numeroFacture = str(dernierNumeroFacture.facture_senso)

        dateArrivee = dt.strptime(data["date_arrivee"], "%d-%m-%Y")
        dateDepart = dt.strptime(data["date_depart"], "%d-%m-%Y")
        nombreJours = (dateDepart - dateArrivee).days + 1

        facture = Facture()
        facture.emetteur = data["emetteur_facture"]
        facture.client = Client.objects.filter(id=data["client"])[0]
        facture.numero_facture = numeroFacture
        facture.numero_commande = data["numero_commande"]
        facture.date_arrivee = dateArrivee
        facture.date_depart = dateDepart
        facture.nombre_jours = nombreJours
        facture.remarques = data["remarques"]

        facture.save()
        dernierNumeroFacture.save()

        context = {
            "etape": "Facture enregistrée",
            "emetteurFacture": data["emetteur_facture"],
            "numeroFacture": numeroFacture,
        }
    else:
        form = AjouterFacture(request.POST or None)
        context = {"form": form, "etape": "Création facture"}

    return render(request, template_name, context)


def test(request):

    template_name = "webpages/test.html"

    """
    context = {"name": "Nathalie Guillaume", "date": "2020-11-12"}
    pdf = render_to_pdf(template_name, context)

    return HttpResponse(pdf, content_type="application/pdf")
    """

    """
    factures = Facture.objects.all()
    facture = factures[0]
    context = CalculerTotauxFacture(facture)

    client = Client.objects.filter(nom_client="Client 1")[0]

    numFactures = []
    for facture in client.factures.all():
        numFactures.append(facture.numero_facture)
    if len(numFactures) == 0:
        facturesClient = "Aucune facture"
    else:
        facturesClient = ", ".join(numFactures)

    context["nom_client"] = client.nom_client
    context["mail_client"] = client.mail_client
    context["adresse_client"] = client.adresse_client
    context["factures_client"] = facturesClient

    """

    facture = Facture.objects.filter(numero_facture="Facture 2")

    resultat = CalculerTotauxParTva(facture[0])

    context = {"dicoTaxesTva": resultat}

    return render(request, template_name, context)
