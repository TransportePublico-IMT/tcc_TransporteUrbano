# Generated by Django 3.0.6 on 2020-10-11 16:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('evento', '0002_auto_20201011_1257'),
    ]

    operations = [
        migrations.AddField(
            model_name='evento',
            name='data_info',
            field=models.CharField(max_length=500, null=True),
        ),
        migrations.AlterField(
            model_name='evento',
            name='data',
            field=models.DateField(null=True),
        ),
    ]