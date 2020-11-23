from import_export.admin import ImportExportModelAdmin
from django.contrib import admin

from .models import *

# Register your models here.


@admin.register(Client)
class ClientResource(ImportExportModelAdmin):
    list_display = [
        "id",
        "nom_client",
        "adresse_client",
        "mail_client",
        "telephone_client",
    ]


@admin.register(Dernier_Numero_Facture)
class Dernier_Numero_FactureResource(ImportExportModelAdmin):
    list_display = [
        "id",
        "facture_asso",
        "facture_senso",
    ]


@admin.register(Facture)
class FactureResource(ImportExportModelAdmin):
    list_display = [
        "id",
        "emetteur",
        "client",
        "numero_facture",
        "numero_commande",
        "date_arrivee",
        "date_depart",
        "montant_paiement_arrhes",
        "modes_paiement_arrhes",
        "date_paiement_arrhes",
        "montant_paiement_solde",
        "modes_paiement_solde",
        "date_paiement_solde",
        "total",
        "remarques",
    ]


@admin.register(Personne)
class PersonneResource(ImportExportModelAdmin):
    list_display = [
        "id",
        "nom_personne",
        "prenom_personne",
        "date_naissance",
        "assujettie_taxe_sejour",
        "alimentation",
        "medicament",
        "remarques",
    ]


@admin.register(Personne_Facture)
class Personne_FactureResource(ImportExportModelAdmin):
    list_display = [
        "id",
        "personne",
        "facture",
    ]


@admin.register(Service_Produit)
class Service_ProduitResource(ImportExportModelAdmin):
    list_display = [
        "id",
        "nom_service_produit",
        "type_service_produit",
        "prix_unitaire",
    ]


@admin.register(Service_Produit_Commande)
class Service_Produit_CommandeResource(ImportExportModelAdmin):
    list_display = [
        "id",
        "service_produit",
        "facture",
        "quantite",
        "prix_total_ht",
        "remise",
        "date_commande",
    ]


@admin.register(Taxe)
class TaxeResource(ImportExportModelAdmin):
    list_display = [
        "id",
        "nom_taxe",
        "initiales",
        "type_taxe",
        "taux",
        "mini",
        "montant_fixe",
    ]


@admin.register(Taxe_Service_Produit)
class Taxe_Service_ProduitResource(ImportExportModelAdmin):
    list_display = ["id", "service_produit", "taxe"]