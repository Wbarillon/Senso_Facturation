from django.db import models

# Create your models here.

"""
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
"""


class Client(models.Model):
    id = models.AutoField(primary_key=True)
    nom_client = models.CharField(
        verbose_name="Nom", max_length=50, null=True, blank=True
    )
    adresse_client = models.CharField(
        verbose_name="Adresse", max_length=200, null=True, blank=True
    )
    mail_client = models.CharField(
        verbose_name="Mail", max_length=100, null=True, blank=True
    )
    telephone_client = models.CharField(
        verbose_name="Téléphone", max_length=50, null=True, blank=True
    )

    def __str__(self):
        return self.nom_client

    class Meta:
        verbose_name = "Client"
        verbose_name_plural = "Clients"


class Personne(models.Model):
    id = models.AutoField(primary_key=True)
    nom_personne = models.CharField(
        verbose_name="Nom", max_length=50, null=True, blank=True
    )
    prenom_personne = models.CharField(
        verbose_name="Prénom", max_length=50, null=True, blank=True
    )
    date_naissance = models.DateField(
        verbose_name="Date de naissance", null=True, blank=True
    )

    def __str__(self):
        return self.nom_personne

    class Meta:
        verbose_name = "Personne"
        verbose_name_plural = "Personnes"


class Personne_Facture(models.Model):
    id = models.AutoField(primary_key=True)
    id_personne = models.ForeignKey(
        "Personne",
        on_delete=models.PROTECT,
        verbose_name="Identifiant Personne",
        related_name="facture_personne",
        null=True,
        blank=True,
    )
    id_facture = models.ForeignKey(
        "Facture",
        on_delete=models.PROTECT,
        verbose_name="Identifiant Facture",
        related_name="personne_facture",
        null=True,
        blank=True,
    )
    assujettie_taxe_sejour = models.BooleanField(
        verbose_name="Assujettie à la taxe de séjour", null=True, blank=True
    )
    alimentation = models.TextField(verbose_name="Alimentation", null=True, blank=True)
    medicament = models.TextField(verbose_name="Médicament", null=True, blank=True)
    remarques = models.TextField(verbose_name="Remarques", null=True, blank=True)


class Service_Produit(models.Model):
    id = models.AutoField(primary_key=True)
    nom_service_produit = models.CharField(
        verbose_name="Nom", max_length=50, null=True, blank=True
    )
    type_service_produit = models.CharField(
        verbose_name="Type", max_length=50, null=True, blank=True
    )
    # On teste comme ça, si il y a des problèmes d'arrondis, switcher avec un type Float
    prix_unitaire = models.DecimalField(
        verbose_name="Prix Unitaire",
        max_digits=8,
        decimal_places=2,
        null=True,
        blank=True,
    )

    def __str__(self):
        return self.nom_service_produit

    class Meta:
        verbose_name = "Service/Produit"
        verbose_name_plural = "Services/Produits"


class Service_Produit_Commande(models.Model):
    id = models.AutoField(primary_key=True)
    id_service_produit = models.ForeignKey(
        "Service_Produit",
        on_delete=models.PROTECT,
        verbose_name="Service commandé",
        related_name="service_produit_commande",
        null=True,
        blank=True,
    )
    id_facture = models.ForeignKey(
        "Facture",
        on_delete=models.PROTECT,
        verbose_name="Facture",
        related_name="service_produit_commande",
        null=True,
        blank=True,
    )
    quantite = models.IntegerField(verbose_name="Quantité", null=True, blank=True)
    # On teste comme ça, si il y a des problèmes d'arrondis, switcher avec un type Float
    prix_total_ht = models.DecimalField(
        verbose_name="Prix Total HT",
        max_digits=8,
        decimal_places=2,
        null=True,
        blank=True,
    )
    remise = models.DecimalField(
        verbose_name="Remise", max_digits=8, decimal_places=2, null=True, blank=True
    )
    arrhes = models.DecimalField(
        verbose_name="Arrhes", max_digits=8, decimal_places=2, null=True, blank=True
    )
    date_commande = models.DateField(
        verbose_name="Date de commande", null=True, blank=True
    )

    class Meta:
        verbose_name = "Service/Produit commandé"
        verbose_name_plural = "Services/Produits commandés"


class Taxe(models.Model):
    id = models.AutoField(primary_key=True)
    nom_taxe = models.CharField(
        verbose_name="Nom", max_length=50, null=True, blank=True
    )
    initiales = models.CharField(
        verbose_name="Initiales", max_length=10, null=True, blank=True
    )
    taux = models.DecimalField(
        verbose_name="Taux", max_digits=4, decimal_places=2, null=True, blank=True
    )
    mini = models.DecimalField(
        verbose_name="Minimal", max_digits=4, decimal_places=2, null=True, blank=True
    )
    montant_fixe = models.DecimalField(
        verbose_name="Montant", max_digits=4, decimal_places=2, null=True, blank=True
    )


class Taxe_Service_Produit(models.Model):
    id = models.AutoField(primary_key=True)
    id_service_produit = models.ForeignKey(
        "Service_Produit",
        on_delete=models.PROTECT,
        verbose_name="Service/produit",
        related_name="taxe_service_produit",
        null=True,
        blank=True,
    )
    id_taxe = models.ForeignKey(
        "Taxe",
        on_delete=models.PROTECT,
        verbose_name="Taxe Service/Produit",
        related_name="taxe_service_produit",
        null=True,
        blank=True,
    )


class Taxe_Service_Produit_Commande(models.Model):
    id = models.AutoField(primary_key=True)
    id_service_produit_commande = models.ForeignKey(
        "Service_Produit_Commande",
        on_delete=models.PROTECT,
        verbose_name="Service/produit commandé",
        related_name="taxe_service_produit_commande",
        null=True,
        blank=True,
    )
    id_taxe = models.ForeignKey(
        "Taxe",
        on_delete=models.PROTECT,
        verbose_name="Taxe Service/Produit Commandé",
        related_name="taxe_service_produit_commande",
        null=True,
        blank=True,
    )


class Facture(models.Model):
    id = models.AutoField(primary_key=True)
    emetteur = models.CharField(
        verbose_name="Emetteur de la facture",
        choices=[("", ""), ("Asso", "Association"), ("Senso", "Sensoryalis")],
        default="",
    )
    id_client = models.ForeignKey(
        "Client",
        on_delete=models.PROTECT,
        verbose_name="Client",
        related_name="facture",
        null=True,
        blank=True,
    )
    dernier_numero_facture_asso = models.IntegerField(
        verbose_name="Dernier numéro de facture Association",
        default=0,
        null=True,
        blank=True,
    )
    dernier_numero_facture_senso = models.IntegerField(
        verbose_name="Dernier numéro de facture Sensoryalis",
        default=10000,
        null=True,
        blank=True,
    )
    numero_facture = models.IntegerField(
        verbose_name="Numéro de la facture", null=True, blank=True
    )
    numero_commande = models.CharField(
        verbose_name="Numéro de la commande", max_length=50, null=True, blank=True
    )
    total = models.DecimalField(
        verbose_name="Total Facture",
        max_digits=8,
        decimal_places=2,
        null=True,
        blank=True,
    )
    reste_a_payer = models.DecimalField(
        verbose_name="Reste à payer",
        max_digits=8,
        decimal_places=2,
        null=True,
        blank=True,
    )
    date_arrivee = models.DateField(
        verbose_name="Date d'arrivée", null=True, blank=True
    )
    date_depart = models.DateField(verbose_name="Date de départ", null=True, blank=True)
    remarques = models.TextField(verbose_name="Remarques", null=True, blank=True)

    def __int__(self):
        return self.numero_facture

    def generer_numero_facture:
        if self.emetteur == "Asso":
            self.dernier_numero_facture_asso += 1
            self.numero_facture = self.dernier_numero_facture_asso
        elif self.emetteur == "Senso":
            self.dernier_numero_facture_senso += 1
            self.numero_facture = self.dernier_numero_facture_senso

    class Meta:
        verbose_name = "Facture"
        verbose_name_plural = "Factures"
