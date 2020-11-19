# Generated by Django 3.1 on 2020-11-19 11:45

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('Senso_facturation_app', '0003_taxe_initiales'),
    ]

    operations = [
        migrations.CreateModel(
            name='Client',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('nom_client', models.CharField(blank=True, max_length=50, null=True, verbose_name='Nom')),
                ('adresse_client', models.CharField(blank=True, max_length=200, null=True, verbose_name='Adresse')),
                ('mail_client', models.CharField(blank=True, max_length=100, null=True, verbose_name='Mail')),
                ('telephone_client', models.CharField(blank=True, max_length=50, null=True, verbose_name='Téléphone')),
            ],
            options={
                'verbose_name': 'Client',
                'verbose_name_plural': 'Clients',
            },
        ),
        migrations.CreateModel(
            name='Facture',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('emetteur', models.CharField(choices=[('', ''), ('Asso', 'Association'), ('Senso', 'Sensoryalis')], default='', max_length=5, verbose_name='Emetteur de la facture')),
                ('dernier_numero_facture_asso', models.IntegerField(blank=True, default=0, null=True, verbose_name='Dernier numéro de facture Association')),
                ('dernier_numero_facture_senso', models.IntegerField(blank=True, default=10000, null=True, verbose_name='Dernier numéro de facture Sensoryalis')),
                ('numero_facture', models.IntegerField(blank=True, null=True, verbose_name='Numéro de la facture')),
                ('numero_commande', models.CharField(blank=True, max_length=50, null=True, verbose_name='Numéro de la commande')),
                ('date_arrivee', models.DateField(blank=True, null=True, verbose_name="Date d'arrivée")),
                ('date_depart', models.DateField(blank=True, null=True, verbose_name='Date de départ')),
                ('montant_paiement_arrhes', models.DecimalField(blank=True, decimal_places=2, max_digits=8, null=True, verbose_name='Montant des arrhes')),
                ('modes_paiement_arrhes', models.TextField(blank=True, null=True, verbose_name='Modes de paiement des arrhes')),
                ('date_paiement_arrhes', models.DateField(blank=True, null=True, verbose_name='Date de paiement des arrhes')),
                ('montant_paiement_solde', models.DecimalField(blank=True, decimal_places=2, max_digits=8, null=True, verbose_name='Montant du solde')),
                ('modes_paiement_solde', models.TextField(blank=True, null=True, verbose_name='Modes de paiement du solde')),
                ('date_paiement_solde', models.DateField(blank=True, null=True, verbose_name='Date de paiement du solde')),
                ('total', models.DecimalField(blank=True, decimal_places=2, max_digits=8, null=True, verbose_name='Total Facture')),
                ('remarques', models.TextField(blank=True, null=True, verbose_name='Remarques')),
                ('id_client', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, related_name='facture', to='Senso_facturation_app.client', verbose_name='Client')),
            ],
            options={
                'verbose_name': 'Facture',
                'verbose_name_plural': 'Factures',
            },
        ),
        migrations.CreateModel(
            name='Personne_Facture',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('id_facture', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, related_name='personne_facture', to='Senso_facturation_app.facture', verbose_name='Identifiant Facture')),
            ],
        ),
        migrations.CreateModel(
            name='Service_Produit_Commande',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('quantite', models.IntegerField(blank=True, null=True, verbose_name='Quantité')),
                ('prix_total_ht', models.DecimalField(blank=True, decimal_places=2, max_digits=8, null=True, verbose_name='Prix Total HT')),
                ('remise', models.DecimalField(blank=True, decimal_places=2, max_digits=8, null=True, verbose_name='Remise')),
                ('arrhes', models.DecimalField(blank=True, decimal_places=2, max_digits=8, null=True, verbose_name='Arrhes')),
                ('date_commande', models.DateField(blank=True, null=True, verbose_name='Date de commande')),
                ('id_facture', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, related_name='service_produit_commande', to='Senso_facturation_app.facture', verbose_name='Facture')),
            ],
            options={
                'verbose_name': 'Service/Produit commandé',
                'verbose_name_plural': 'Services/Produits commandés',
            },
        ),
        migrations.CreateModel(
            name='Taxe_Service_Produit',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
            ],
        ),
        migrations.CreateModel(
            name='Taxe_Service_Produit_Commande',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('id_service_produit_commande', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, related_name='taxe_service_produit_commande', to='Senso_facturation_app.service_produit_commande', verbose_name='Service/produit commandé')),
            ],
        ),
        migrations.RemoveField(
            model_name='sejour',
            name='id_commande',
        ),
        migrations.AlterModelOptions(
            name='service_produit',
            options={'verbose_name': 'Service/Produit', 'verbose_name_plural': 'Services/Produits'},
        ),
        migrations.RenameField(
            model_name='personne',
            old_name='naissance_date',
            new_name='date_naissance',
        ),
        migrations.RemoveField(
            model_name='service_produit',
            name='id_taxe',
        ),
        migrations.RemoveField(
            model_name='service_produit',
            name='prix',
        ),
        migrations.AddField(
            model_name='personne',
            name='assujettie_taxe_sejour',
            field=models.BooleanField(blank=True, null=True, verbose_name='Assujettie à la taxe de séjour'),
        ),
        migrations.AddField(
            model_name='personne',
            name='prenom_personne',
            field=models.CharField(blank=True, max_length=50, null=True, verbose_name='Prénom'),
        ),
        migrations.AddField(
            model_name='service_produit',
            name='prix_unitaire',
            field=models.DecimalField(blank=True, decimal_places=2, max_digits=8, null=True, verbose_name='Prix Unitaire'),
        ),
        migrations.AddField(
            model_name='taxe',
            name='mini',
            field=models.DecimalField(blank=True, decimal_places=2, max_digits=4, null=True, verbose_name='Minimal'),
        ),
        migrations.AddField(
            model_name='taxe',
            name='montant_fixe',
            field=models.DecimalField(blank=True, decimal_places=2, max_digits=4, null=True, verbose_name='Montant'),
        ),
        migrations.DeleteModel(
            name='Commande',
        ),
        migrations.DeleteModel(
            name='Sejour',
        ),
        migrations.AddField(
            model_name='taxe_service_produit_commande',
            name='id_taxe',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, related_name='taxe_service_produit_commande', to='Senso_facturation_app.taxe', verbose_name='Taxe Service/Produit Commandé'),
        ),
        migrations.AddField(
            model_name='taxe_service_produit',
            name='id_service_produit',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, related_name='taxe_service_produit', to='Senso_facturation_app.service_produit', verbose_name='Service/produit'),
        ),
        migrations.AddField(
            model_name='taxe_service_produit',
            name='id_taxe',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, related_name='taxe_service_produit', to='Senso_facturation_app.taxe', verbose_name='Taxe Service/Produit'),
        ),
        migrations.AddField(
            model_name='service_produit_commande',
            name='id_service_produit',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, related_name='service_produit_commande', to='Senso_facturation_app.service_produit', verbose_name='Service commandé'),
        ),
        migrations.AddField(
            model_name='personne_facture',
            name='id_personne',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, related_name='facture_personne', to='Senso_facturation_app.personne', verbose_name='Identifiant Personne'),
        ),
    ]
