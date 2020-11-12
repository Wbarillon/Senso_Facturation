from django.db import models

# Create your models here.

'''
Un produit ou un service manque ? Il suffit de le créer.
forms => AddProduct / AddService

La facture est générée à partir des informations issues de la requête suivante :
SELECT *
FROM Commande
WHERE Personne = id / nom_personne
AND commande_date = la date

ou, si c'est dans le cadre d'un séjour avec hébergement :
AND arrivee_date = la date

Globalement, la facture c'est lié à une personne dans le temps. Et "indirectement", on chope les commandes et l'hebergement.

Parmi les services, il y a location d'une salle sur une durée (une semaine). Ça va où ?
Il y a service salle_activite_semaine et salle_activite_we.


Personne
id
nom_personne
naissance_date
alimentation
medicament
remarques

Incertitude sur la tva. A priori c'est juste un entier mais il y a peut-être plusieurs taxes pour un même service ?

Taxe
id
nom
initiales
taux

Service_Produit
id
id_taxe
nom
type (repas, chambre, salle, vente à emporter, vente sur place...)
prix

Commande
id
id_personne
id_service_produit
arrhes (non ou le prix)
commande_date

Sejour
id
id_commande
arrivee_date
depart_date
'''

class Personne(models.Model):
    id = models.AutoField(primary_key = True)
    nom_personne = models.CharField(verbose_name = 'Nom', max_length = 50, null = True, blank = True)
    naissance_date = models.DateField(verbose_name = 'Date de naissance', null = True, blank = True)
    alimentation = models.TextField(verbose_name = 'Alimentation', null = True, blank = True)
    medicament = models.TextField(verbose_name = 'Médicament', null = True, blank = True)
    remarques = models.TextField(verbose_name = 'Remarques', null = True, blank = True)

    def __str__(self):
        return self.nom_personne

    class Meta:
        verbose_name = 'Personne'
        verbose_name_plural = 'Personnes'

class Service_Produit(models.Model):
    id = models.AutoField(primary_key = True)
    id_taxe = models.ForeignKey('Taxe', on_delete = models.PROTECT, verbose_name = 'Taxe', related_name = 'service_produit_taxe', null = True, blank = True)
    nom_service_produit = models.CharField(verbose_name = 'Nom', max_length = 50, null = True, blank = True)
    type_service_produit = models.CharField(verbose_name = 'Type', max_length = 50, null = True, blank = True)
    # On teste comme ça, si il y a des problèmes d'arrondis, switcher avec un type Float
    prix = models.DecimalField(verbose_name = 'Prix', max_digits = 8, decimal_places = 2, null = True, blank = True)

    def __str__(self):
        return self.nom_service_produit

    class Meta:
        verbose_name = 'Service / Produit'
        verbose_name_plural = 'Services / Produits'

class Taxe(models.Model):
    id = models.AutoField(primary_key = True)
    nom_taxe = models.CharField(verbose_name = 'Nom', max_length = 50, null = True, blank = True)
    initiales = models.CharField(verbose_name = 'Initiales', max_length = 10, null = True, blank = True)
    taux = models.DecimalField(verbose_name = 'Taux', max_digits = 4, decimal_places = 2, null = True, blank = True)

class Commande(models.Model):
    id = models.AutoField(primary_key = True)
    id_personne = models.ForeignKey('Personne', on_delete = models.PROTECT, verbose_name = 'Personne', related_name = 'commande_personne', null = True, blank = True)
    id_service_produit = models.ForeignKey('Service_Produit', on_delete = models.PROTECT, verbose_name = 'Service / Produit', related_name = 'commande_service_produit', null = True, blank = True)
    arrhes = models.DecimalField(verbose_name = 'Arrhes', max_digits = 8, decimal_places = 2, null = True, blank = True)
    commande_date = models.DateField(verbose_name = 'Date de commande', null = True, blank = True)

    def __int__(self):
        return self.id

    class Meta:
        verbose_name = 'Commande'
        verbose_name_plural = 'Commandes'

class Sejour(models.Model):
    id = models.AutoField(primary_key = True)
    id_commande = models.ForeignKey('Commande', on_delete = models.PROTECT, verbose_name = 'Commande', related_name = 'sejour_id_commande', null = True, blank = True)
    arrivee_date = models.DateField(verbose_name = 'Date d\'arrivée', null = True, blank = True)
    depart_date = models.DateField(verbose_name = 'Date de départ', null = True, blank = True)

    def __int__(self):
        return self.id

    class Meta:
        verbose_name = 'Séjour'
        verbose_name_plural = 'Séjours'