# Generated by Django 3.0.6 on 2020-08-22 13:37

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('onibus', '0007_onibusposicao_sentido'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='onibusposicao',
            name='sentido',
        ),
    ]
