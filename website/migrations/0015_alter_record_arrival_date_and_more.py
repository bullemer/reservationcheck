# Generated by Django 5.0.1 on 2024-02-01 23:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('website', '0014_alter_record_response_untill'),
    ]

    operations = [
        migrations.AlterField(
            model_name='record',
            name='arrival_date',
            field=models.DateField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='record',
            name='response_untill',
            field=models.DateField(blank=True, null=True),
        ),
    ]
