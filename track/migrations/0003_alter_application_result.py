# Generated by Django 4.1.7 on 2023-02-19 19:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('track', '0002_application_position'),
    ]

    operations = [
        migrations.AlterField(
            model_name='application',
            name='result',
            field=models.CharField(choices=[('accepted', 'accepted'), ('rejected', 'rejected'), ('under consideration', 'under consideration')], max_length=50),
        ),
    ]
