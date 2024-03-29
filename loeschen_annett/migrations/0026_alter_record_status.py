# Generated by Django 5.0.1 on 2024-02-14 16:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('website', '0025_delete_email_delete_emaillog_delete_emailtemplate'),
    ]

    operations = [
        migrations.AlterField(
            model_name='record',
            name='status',
            field=models.CharField(blank=True, choices=[('UNANSWERED', 'CREATED'), ('EMAIL SEND', 'EMAIL SEND'), ('ANSWERED', 'ANSWERED'), ('FINISH', 'FINISH')], default='UNANSWERED', max_length=20),
        ),
    ]
