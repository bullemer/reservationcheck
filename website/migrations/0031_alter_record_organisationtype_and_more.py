# Generated by Django 5.0.1 on 2024-02-18 16:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('website', '0030_rename_planned_depature_time_record_planned_departure_time'),
    ]

    operations = [
        migrations.AlterField(
            model_name='record',
            name='organisationtype',
            field=models.CharField(blank=True, choices=[('Schule', 'Schule'), ('Verein', 'Verein'), ('Uni', 'Uni'), ('Projekt', 'Projekt')], default=None, max_length=20),
        ),
        migrations.AlterField(
            model_name='record',
            name='traveldetail',
            field=models.CharField(blank=True, choices=[('San Pepelone Reisebus', 'San Pepelone Reisebus'), ('Eigener Bus', 'Eigener Bus'), ('Bahn', 'Bahn'), ('PKW', 'PKW')], default=None, max_length=40),
        ),
    ]
