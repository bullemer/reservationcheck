# Generated by Django 5.0.1 on 2024-02-01 23:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('website', '0013_record_status'),
    ]

    operations = [
        migrations.AlterField(
            model_name='record',
            name='response_untill',
            field=models.DateTimeField(blank=True, null=True),
        ),
    ]
