from import_export.admin import ImportExportModelAdmin
from django.contrib import admin

from .models import *

# Register your models here.

@admin.register(Personne)
class PersonneResource(ImportExportModelAdmin):
    list_display = ['id', 'nom_personne', 'naissance_date', 'alimentation', 'medicament', 'remarques']

@admin.register(Service_Produit)
class Service_ProduitResource(ImportExportModelAdmin):
    list_display = ['id', 'nom_service_produit', 'type_service_produit', 'prix']

@admin.register(Taxe)
class TaxeResource(ImportExportModelAdmin):
    list_display = ['id', 'nom_taxe', 'taux']

@admin.register(Commande)
class CommandeResource(ImportExportModelAdmin):
    list_display = ['id', 'id_personne', 'id_service_produit', 'arrhes', 'commande_date']

@admin.register(Sejour)
class SejourResource(ImportExportModelAdmin):
    list_display = ['id', 'id_commande', 'arrivee_date', 'depart_date']
