# Generated by Django 4.0 on 2022-04-25 08:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mainapp', '0003_users_email'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='extraproducts',
            options={'verbose_name': 'Допы', 'verbose_name_plural': 'Допы'},
        ),
        migrations.CreateModel(
            name='SetsExtraProducts',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(help_text='Введите название', max_length=255, verbose_name='Название')),
                ('extra', models.ManyToManyField(related_name='extra', to='mainapp.ExtraProducts', verbose_name='Доп')),
            ],
            options={
                'verbose_name': 'Допы',
                'verbose_name_plural': 'Допы',
            },
        ),
    ]
