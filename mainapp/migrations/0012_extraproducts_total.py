# Generated by Django 4.0 on 2022-04-26 13:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mainapp', '0011_rename_set_dops_flowers_set'),
    ]

    operations = [
        migrations.AddField(
            model_name='extraproducts',
            name='total',
            field=models.PositiveIntegerField(blank=True, null=True),
        ),
    ]
