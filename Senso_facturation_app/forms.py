from unicodedata2 import normalize
from functools import partial

from django import forms

from .models import *

DatePicker = partial(forms.DateInput, {"class": "datepicker"})


class AjouterFacture(forms.Form):

    emetteur_facture = forms.ChoiceField(
        choices=[("", ""), ("Asso", "Association"), ("Senso", "Sensoryalis")],
        label="Emetteur de la facture",
    )

    clients = Client.objects.all()
    choice_clients = [("", "")]
    for client in clients:
        choice_clients.append((client.id, client.nom_client))
    client = forms.ChoiceField(choices=choice_clients, label="Client")

    numero_commande = forms.CharField(label="Numéro de la commande", max_length=50)

    date_arrivee = forms.DateField(label="Date d'arrivée", widget=DatePicker())

    date_depart = forms.DateField(label="Date de départ", widget=DatePicker())

    remarques = forms.CharField(widget=forms.Textarea, label="Remarques")

    def __init__(self, *args, **kwargs):

        super(AjouterFacture, self).__init__(*args, **kwargs)
