# Generated by Django 4.0 on 2022-04-26 15:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mainapp', '0014_extraproducts_col_alter_extraproducts_selected_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='flowers',
            name='col',
            field=models.PositiveIntegerField(default=1, verbose_name='техническое поле, не трогать'),
        ),
    ]
