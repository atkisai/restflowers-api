# Generated by Django 4.0 on 2022-04-04 15:07

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Order',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('email', models.CharField(max_length=255, verbose_name='Почта')),
                ('fio', models.CharField(max_length=255, verbose_name='ФИО')),
                ('phone', models.CharField(max_length=255, verbose_name='Телефон')),
                ('city', models.CharField(max_length=255, verbose_name='Город проживания')),
                ('city_fr', models.CharField(max_length=255, null=True, verbose_name='В каком городе открыть')),
                ('brend', models.CharField(max_length=255, verbose_name='Бренд')),
                ('kapital', models.CharField(max_length=255, verbose_name='Капитал')),
                ('opit', models.CharField(max_length=255, verbose_name='Опыт в предпринимательстве')),
                ('obopite', models.TextField(verbose_name='Опыт в бинессе')),
                ('velbiznes', models.CharField(max_length=255, verbose_name='Скем вел бизнесс')),
                ('pochemu', models.TextField(verbose_name='Почему хотите приобрести')),
                ('date_add', models.DateTimeField(auto_now_add=True, verbose_name='Дата добавление')),
            ],
            options={
                'verbose_name': 'Заявка',
                'verbose_name_plural': 'Заявки',
                'ordering': ['-date_add'],
            },
        ),
    ]