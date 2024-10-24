# Generated by Django 5.1.2 on 2024-10-24 13:19

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cnc_app', '0003_detailentree_date_ajout_detailinventaire_date_ajout'),
    ]

    operations = [
        migrations.AddField(
            model_name='designation',
            name='famille',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='cnc_app.famille'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='designation',
            name='marque',
            field=models.CharField(default='non-spécifié', max_length=100),
        ),
        migrations.AddField(
            model_name='designation',
            name='modele',
            field=models.CharField(default='non-spécifié', max_length=100),
        ),
    ]
