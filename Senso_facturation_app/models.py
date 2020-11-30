from django.db import models
from django.core.exceptions import ValidationError

# Create your models here.


class Client(models.Model):
    id = models.AutoField(primary_key=True)
    nom_client = models.CharField(
        verbose_name="Nom", max_length=50, unique=True, default=""
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
        ordering = ["nom_client"]


class Dernier_Numero_Facture(models.Model):
    id = models.AutoField(primary_key=True)
    facture_asso = models.IntegerField(
        verbose_name="Dernier numéro de facture Association",
        default=0,
        null=True,
        blank=True,
    )
    facture_senso = models.IntegerField(
        verbose_name="Dernier numéro de facture Sensoryalis",
        default=10000,
        null=True,
        blank=True,
    )


class Facture(models.Model):
    id = models.AutoField(primary_key=True)
    emetteur = models.CharField(
        verbose_name="Emetteur de la facture",
        max_length=20,
        choices=[("", ""), ("Asso", "Association"), ("Senso", "Sensoryalis")],
        default="",
        null=True,
        blank=True,
    )
    client = models.ForeignKey(
        "Client",
        on_delete=models.PROTECT,
        verbose_name="Client",
        related_name="factures",
        null=True,
        blank=True,
    )
    personnes = models.ManyToManyField("Personne", through="Personne_Facture")
    numero_facture = models.CharField(
        verbose_name="Numéro de la facture", max_length=30, null=True, blank=True
    )
    numero_commande = models.CharField(
        verbose_name="Numéro de la commande", max_length=50, null=True, blank=True
    )
    date_arrivee = models.DateField(
        verbose_name="Date d'arrivée", null=True, blank=True
    )
    date_depart = models.DateField(verbose_name="Date de départ", null=True, blank=True)
    nombre_jours = models.IntegerField(
        verbose_name="Nombre de jours", null=True, blank=True
    )
    remarques = models.TextField(verbose_name="Remarques", null=True, blank=True)

    def __str__(self):
        return self.numero_facture

    class Meta:
        verbose_name = "Facture"
        verbose_name_plural = "Factures"


class Paiement(models.Model):
    id = models.AutoField(primary_key=True)
    service_produit_commande = models.ForeignKey(
        "Service_Produit_Commande",
        on_delete=models.PROTECT,
        verbose_name="Service/Produit commandé",
        related_name="paiements",
        null=True,
        blank=True,
    )
    montant_paiement = models.DecimalField(
        verbose_name="Montant du paiement",
        max_digits=8,
        decimal_places=2,
        null=True,
        blank=True,
    )
    type_paiement = models.CharField(
        verbose_name="Type de paiement",
        max_length=10,
        choices=[("", ""), ("Arrhes", "Arrhes"), ("Solde", "Solde")],
        default="",
    )
    mode_paiement = models.CharField(
        verbose_name="Mode de paiement",
        max_length=30,
        choices=[
            ("", ""),
            ("Chèque", "Chèque"),
            ("Chèques Vacances", "Chèques Vacances"),
            ("Carte de Crédit", "Carte de Crédit"),
            ("Carte Tickets Restaurant", "Carte Tickets Restaurant"),
            ("Liquide", "Liquide"),
            ("Tickets Restaurant", "Tickets Restaurant"),
            ("Virement Bancaire", "Virement Bancaire"),
        ],
        null=True,
        blank=True,
    )
    numero_cheque = models.CharField(
        verbose_name="Numéro du chèque",
        max_length=20,
        null=True,
        blank=True,
    )
    date_paiement = models.DateField(
        verbose_name="Date de paiement", null=True, blank=True
    )

    def __str__(self):
        return (
            self.service_produit_commande.service_produit.nom_service_produit
            + " ("
            + str(self.date_paiement)
            + ")"
        )

    class Meta:
        verbose_name = "Paiement"
        verbose_name_plural = "Paiements"


class Personne(models.Model):
    id = models.AutoField(primary_key=True)
    nom_personne = models.CharField(verbose_name="Nom", max_length=50, default="")
    prenom_personne = models.CharField(verbose_name="Prénom", max_length=50, default="")
    date_naissance = models.DateField(
        verbose_name="Date de naissance", null=True, blank=True
    )
    adresse_personne = models.CharField(
        verbose_name="Adresse", max_length=200, null=True, blank=True
    )
    mail_personne = models.CharField(
        verbose_name="Mail", max_length=100, null=True, blank=True
    )
    telephone_personne = models.CharField(
        verbose_name="Téléphone", max_length=50, null=True, blank=True
    )
    assujettie_taxe_sejour = models.BooleanField(
        verbose_name="Assujettie à la taxe de séjour", null=True, blank=True
    )
    alimentation = models.TextField(verbose_name="Alimentation", null=True, blank=True)
    medicament = models.TextField(verbose_name="Médicament", null=True, blank=True)
    remarques = models.TextField(verbose_name="Remarques", null=True, blank=True)

    def __str__(self):
        return self.prenom_personne + " " + self.nom_personne

    class Meta:
        verbose_name = "Personne"
        verbose_name_plural = "Personnes"
        unique_together = ("nom_personne", "prenom_personne")
        ordering = ["nom_personne", "prenom_personne"]


class Personne_Facture(models.Model):
    id = models.AutoField(primary_key=True)
    personne = models.ForeignKey(
        "Personne",
        on_delete=models.PROTECT,
        verbose_name="Personne",
        null=True,
        blank=True,
    )
    facture = models.ForeignKey(
        "Facture",
        on_delete=models.PROTECT,
        verbose_name="Facture",
        null=True,
        blank=True,
    )

    class Meta:
        verbose_name = "Personne/Facture"
        verbose_name_plural = "Personnes/Factures"


class Service_Produit(models.Model):
    id = models.AutoField(primary_key=True)
    nom_service_produit = models.CharField(
        verbose_name="Nom", max_length=50, unique=True, default=""
    )
    type_service_produit = models.CharField(
        verbose_name="Type", max_length=50, default=""
    )
    # On teste comme ça, si il y a des problèmes d'arrondis, switcher avec un type Float
    prix_unitaire = models.DecimalField(
        verbose_name="Prix Unitaire",
        max_digits=8,
        decimal_places=2,
        null=True,
        blank=True,
    )
    taxes = models.ManyToManyField("Taxe", through="Taxe_Service_Produit")

    def __str__(self):
        return self.nom_service_produit + " (" + self.type_service_produit + ")"

    class Meta:
        verbose_name = "Service/Produit"
        verbose_name_plural = "Services/Produits"
        ordering = ["type_service_produit", "nom_service_produit"]


class Service_Produit_Commande(models.Model):
    id = models.AutoField(primary_key=True)
    service_produit = models.ForeignKey(
        "Service_Produit",
        on_delete=models.PROTECT,
        verbose_name="Service/Produit",
        null=True,
        blank=True,
    )
    facture = models.ForeignKey(
        "Facture",
        on_delete=models.PROTECT,
        verbose_name="Facture",
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
    date_commande = models.DateField(
        verbose_name="Date de commande", null=True, blank=True
    )

    def __str__(self):
        return (
            "Facture "
            + self.facture.numero_facture
            + " : "
            + self.service_produit.nom_service_produit
        )

    class Meta:
        verbose_name = "Service/Produit commandé"
        verbose_name_plural = "Services/Produits commandés"


class Taxe(models.Model):
    id = models.AutoField(primary_key=True)
    nom_taxe = models.CharField(
        verbose_name="Nom", max_length=50, unique=True, default=""
    )
    initiales = models.CharField(verbose_name="Initiales", max_length=10, default="")
    type_taxe = models.CharField(
        verbose_name="Type de taxe",
        max_length=30,
        choices=[
            ("", ""),
            ("Taux_Sans_Mini", "Taux sans minimum"),
            ("Taux_Avec_Mini_Global", "Taux avec minimum global"),
            ("Taux_Avec_Mini_Par_Jour", "Taux avec minimum par jour"),
            ("Montant_Fixe_Global", "Montant fixe global"),
            ("Montant_Fixe_Par_Jour", "Montant fixe par jour"),
            ("Type_Taxe_De_Sejour", "Type taxe de séjour"),
        ],
        default="",
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

    def __str__(self):
        return self.nom_taxe

    def clean(self):
        super().clean()
        if self.taux is None and self.montant_fixe is None:
            raise ValidationError(
                "Un des deux champs <taux> et <montant_fixe> doit impérativement être renseigné."
            )

    class Meta:
        verbose_name = "Taxe"
        verbose_name_plural = "Taxes"
        ordering = ["nom_taxe"]


class Taxe_Service_Produit(models.Model):
    id = models.AutoField(primary_key=True)
    service_produit = models.ForeignKey(
        "Service_Produit",
        on_delete=models.PROTECT,
        verbose_name="Service/produit",
        null=True,
        blank=True,
    )
    taxe = models.ForeignKey(
        "Taxe",
        on_delete=models.PROTECT,
        verbose_name="Taxe Service/Produit",
        null=True,
        blank=True,
    )

    class Meta:
        verbose_name = "Taxe/Service/produit"
        verbose_name_plural = "Taxes/Services/Produits"
        ordering = ["service_produit", "taxe"]
