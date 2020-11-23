# Generated by Django 3.1 on 2020-11-23 13:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Senso_facturation_app', '0005_auto_20201122_2152'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='facture',
            name='services_produits',
        ),
        migrations.AddField(
            model_name='personne',
            name='adresse_personne',
            field=models.CharField(blank=True, max_length=200, null=True, verbose_name='Adresse'),
        ),
        migrations.AddField(
            model_name='personne',
            name='mail_personne',
            field=models.CharField(blank=True, max_length=100, null=True, verbose_name='Mail'),
        ),
        migrations.AddField(
            model_name='personne',
            name='telephone_personne',
            field=models.CharField(blank=True, max_length=50, null=True, verbose_name='Téléphone'),
        ),
    ]