# Generated by Django 4.0 on 2022-04-30 18:58

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0003_rename_quantity_order_items_amount_and_more'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='order_items',
            options={'verbose_name': 'Продукты в заказах', 'verbose_name_plural': 'Продукты в заказах'},
        ),
        migrations.AlterModelOptions(
            name='order_items_extra_items',
            options={'verbose_name': 'Допы в заказах', 'verbose_name_plural': 'Допы в заказах'},
        ),
        migrations.AlterField(
            model_name='order_items',
            name='total_price',
            field=models.PositiveIntegerField(verbose_name='Финальная цена'),
        ),
        migrations.AlterField(
            model_name='order_items_extra_items',
            name='order_item',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='extra_item', to='orders.order_items', verbose_name='Заказанный букет'),
        ),
    ]
