# Generated by Django 3.1 on 2020-11-03 15:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Senso_facturation_app', '0002_auto_20201103_1612'),
    ]

    operations = [
        migrations.AddField(
            model_name='taxe',
            name='initiales',
            field=models.CharField(blank=True, max_length=10, null=True, verbose_name='Initiales'),
        ),
    ]
