from unicodedata2 import normalize
from functools import partial

from django import forms

from .models import *

DatePicker = partial(forms.DateInput, {"class": "datepicker"})


class AddFacture(forms.Form):

    emetteur_facture = forms.ChoiceField(
        choices=[("", ""), ("Asso", "Association"), ("Senso", "Sensoryalis")],
        label="Emetteur de la facture",
    )

    clients = Client.objects.all()
    choice_clients = []
    for client in clients:
        choice_clients.append((Client.id, Client.nom_client))
    client = forms.ChoiceField(choices=choice_clients, label="Client")

    numero_commande = forms.CharField(label="Numéro de la commande", max_length=50)

    date_arrivee = forms.DateField(label="Date d'arrivée")

    date_depart = forms.DateField(label="Date de départ")

    nb_jours = forms.IntegerField(label="Nombre de jours")

    montant_arrhes = forms.DecimalField(label="Montant des arrhes", decimal_places=2)
    modes_paiement_arrhes = forms.CharField(widget=forms.Textarea, label="Modes de paiement des arrhes")
    date_paiement_arrhes = forms.DateField(label="Date de paiement des arrhes")

    montant_solde = forms.DecimalField(label="Montant du solde", decimal_places=2)
    modes_paiement_solde = forms.CharField(widget=forms.Textarea, label="Modes de paiement du solde")
    date_paiement_solde = forms.DateField(label="Date de paiement du solde")

    remarques = forms.CharField(widget=forms.Textarea, label="Remarques")

    question = forms.BooleanField(
        label="Voulez-vous enregistrer cette facture ?",
        widget=forms.RadioSelect(
            choices=[("Oui", "Oui"), ("Non", "Non")], attrs={"class": "radio-check"}
        ),
        required=False,
    )

    def __init__(self, *args, **kwargs):

        reponse = kwargs.pop("reponse")

        super(AddFacture, self).__init__(*args, **kwargs)

        """
        if reponse == "Oui":
            self.fields["phase"] = forms.ChoiceField(
                choices=PhaseCulturesChoix.choices,
                required=False,
            )

            self.fields["phase_date"] = forms.DateField(
                widget=DatePicker(), required=False
            )
        """
