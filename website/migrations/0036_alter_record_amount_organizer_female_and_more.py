# Generated by Django 5.0.1 on 2024-02-19 21:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('website', '0035_record_created_by'),
    ]

    operations = [
        migrations.AlterField(
            model_name='record',
            name='amount_organizer_female',
            field=models.PositiveIntegerField(blank=True, default='', null=True),
        ),
        migrations.AlterField(
            model_name='record',
            name='amount_organizer_male',
            field=models.PositiveIntegerField(blank=True, default='', null=True),
        ),
        migrations.AlterField(
            model_name='record',
            name='amount_students_female',
            field=models.PositiveIntegerField(blank=True, default='', null=True),
        ),
        migrations.AlterField(
            model_name='record',
            name='amount_students_male',
            field=models.PositiveIntegerField(blank=True, default='', null=True),
        ),
    ]