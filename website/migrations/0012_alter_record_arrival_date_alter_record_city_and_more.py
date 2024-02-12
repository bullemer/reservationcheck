# Generated by Django 5.0.1 on 2024-02-01 19:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('website', '0011_alter_record_amount_organizer_female_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='record',
            name='arrival_date',
            field=models.DateTimeField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='record',
            name='city',
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
        migrations.AlterField(
            model_name='record',
            name='organisation',
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
        migrations.AlterField(
            model_name='record',
            name='organisationtype',
            field=models.CharField(blank=True, choices=[('Schule', 'Schule'), ('Verein', 'Verein'), ('Uni', 'Uni'), ('Projekt', 'Projekt')], default='Schule', max_length=20),
        ),
        migrations.AlterField(
            model_name='record',
            name='phone',
            field=models.CharField(blank=True, max_length=15, null=True),
        ),
        migrations.AlterField(
            model_name='record',
            name='planned_arrival_time',
            field=models.CharField(blank=True, choices=[('10:00', '10:00'), ('10:30', '10:30'), ('11:00', '11:00'), ('11:30', '11:30'), ('12:00', '12:00'), ('12:30', '12:30'), ('13:00', '13:00'), ('13:30', '13:30'), ('14:00', '14:00'), ('14:30', '14:30'), ('15:00', '15:00'), ('15:30', '15:30'), ('16:00', '16:00'), ('16:30', '16:30'), ('17:00', '17:00'), ('17:30', '17:30'), ('18:00', '18:00'), ('18:30', '18:30'), ('19:00', '19:00'), ('19:30', '19:30'), ('20:00', '20:00'), ('20:30', '20:30')], default=None, max_length=5, null=True),
        ),
    ]