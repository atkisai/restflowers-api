from django.contrib.auth.models import User
from django.db import models
from mainapp.models import Flowers, ExtraProducts, City, Filial


class FasrOrder(models.Model):
    first_name = models.CharField(max_length=50,verbose_name='Имя')
    phone=models.CharField(max_length=255,verbose_name='Телефон')
    flower=models.ForeignKey(Flowers,verbose_name='Цветы',on_delete=models.CASCADE)
    date_add = models.DateTimeField(verbose_name='Дата добавление', auto_now_add=True)
    city = models.ForeignKey(City,on_delete=models.SET_NULL, blank=True, null=True, verbose_name='Город')
    filial = models.ForeignKey(Filial, on_delete=models.SET_NULL, verbose_name='Филиал', blank=True, null=True)
    def __str__(self):
        return f'Быстрая заявка {self.first_name}'
    class Meta:
        verbose_name_plural = 'Быстрая заявка'
        verbose_name = 'Быстрая заявка'
        ordering=['-date_add']

class Order(models.Model):
    times=(
        (('В течение дня','В течение дня')),
        (('7:00-10:00','7:00-10:00')),
        (('10:00-13:00','10:00-13:00')),
        (('13:00-16:00','13:00-16:00')),
        (('16:00-19:00','16:00-19:00')),
        (('19:00-22:00','19:00-22:00')),

    )
    metod_paired=(
        (('Оплата наличными курьеру'),('Оплата наличными курьеру')),
        (('Оплата через Kaspi'),('Оплата через Kaspi')),
        (('Оплата онлайн'),('Оплата онлайн')),
    )
    statuses=(
        (('Новый'),('Новый')),
        (('Оплачен'),('Оплачен')),
        (('Не оплачен'),('Не оплачен')),
        (('Завершен'),('Завершен')),
        (('Собран'),('Собран')),
        (('В пути'),('В пути')),
        (('Возврат'),('Возврат')),
        (('Нереализован'),('Нереализован')),
        (('Доставлен'),('Доставлен')),
    )
    user=models.ForeignKey(User,on_delete=models.CASCADE,verbose_name='Покупатель')
    first_name = models.CharField(max_length=50, verbose_name='Имя')
    recipient_phone = models.CharField(max_length=255, verbose_name='Телефон получателя')
    adres=models.CharField(max_length=255, verbose_name='Адрес')
    date=models.DateField(verbose_name='Дата')
    time=models.CharField(verbose_name='Время',max_length=255,choices=times)
    anonim=models.BooleanField(verbose_name='Анонимно',default=False)
    sended_phone=models.CharField(max_length=255, verbose_name='Телефон отправителя')
    email=models.EmailField(verbose_name='email')
    postcard=models.TextField(verbose_name='Открытка',blank=True,null=True)
    comments=models.TextField(verbose_name='Комментарий',blank=True,null=True)
    paired=models.CharField(verbose_name='Способ оплаты',max_length=255,choices=metod_paired)
    status=models.CharField(verbose_name='Статус',max_length=255,choices=statuses,default='Новый')
    sum_result=models.PositiveIntegerField(verbose_name='Сумма',default=0,blank=True,null=True)
    date_add=models.DateTimeField(verbose_name='Дата добавление',auto_now_add=True)
    likes=(
        (('Букет не собран'),('Букет не собран')),
        (('Букет собран'),('Букет собран')),
        (('Клиент подтвердил'),('Клиент подтвердил')),
        (('Клиент не подтвердил'),('Клиент не подтвердил')),
        (('Заказ доставлен'),('Заказ доставлен')),

    )
    archiv=models.BooleanField(verbose_name='В архиве',default=False)
    like_flower=models.CharField(verbose_name='Фото букета',max_length=255,choices=likes,default='Букет не собран')
    city = models.ForeignKey('mainapp.City',  default=1 ,on_delete=models.SET_NULL, blank=True, null=True, verbose_name='Город')
    filial = models.ForeignKey(Filial, on_delete=models.SET_NULL, verbose_name='Филиал', blank=True, null=True)

    def __str__(self):
        return f'Заявка {self.first_name}'
    class Meta:
        verbose_name_plural = 'Заявки'
        verbose_name = 'Заявки'
        ordering = ['-date_add']


class Order_items(models.Model):
    order = models.ForeignKey(Order,verbose_name='Заявка',on_delete=models.CASCADE, related_name='order_items')
    item = models.ForeignKey(Flowers,on_delete=models.CASCADE,verbose_name='Букет', related_name='order_flowers')
    amount = models.PositiveIntegerField(verbose_name='Количество')
    total_price = models.PositiveIntegerField(verbose_name='Финальная цена')

    def __str__(self):
        return f'Букет {self.id}'

    class Meta:
        verbose_name_plural = 'Продукты в заказах'
        verbose_name = 'Продукты в заказах'


class Order_items_extra_items(models.Model):
    order_item = models.ForeignKey(Order_items,on_delete=models.CASCADE, verbose_name='Заказанный букет', related_name='extra_item')
    extra = models.ForeignKey(ExtraProducts,on_delete=models.CASCADE, verbose_name='Доп',related_name='extra')
    amount = models.PositiveIntegerField(verbose_name='Количество')

    def __str__(self):
        return f'Доп {self.id}'

    class Meta:
        verbose_name_plural = 'Допы в заказах'
        verbose_name = 'Допы в заказах'


class OrderExtra(models.Model):
    order=models.ForeignKey(Order,on_delete=models.CASCADE)
    extra=models.ForeignKey(ExtraProducts,on_delete=models.CASCADE)
    flower=models.ForeignKey(Flowers,on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()
    def __str__(self):
        return f'Корзина продукты '

    class Meta:
        verbose_name_plural = 'Корзина продукта'
        verbose_name = 'Корзина продукта'

class OrderFlowerImage(models.Model):
    order=models.OneToOneField(Order,on_delete=models.CASCADE)
    image=models.FileField(upload_to='ready_flower',blank=True)

    # def __str__(self):
    #     return f'Фото букета {self.order.order_items_set.first()}  '

    class Meta:
        verbose_name_plural = 'Фото букета'
        verbose_name = 'Фото букета'

class OrderKurierImage(models.Model):
    order=models.OneToOneField(Order,on_delete=models.CASCADE)
    image=models.FileField(upload_to='ready_flower',blank=True)

    # def __str__(self):
    #     return f'Фото курьера {self.order.order_items_set.first()}  '

    class Meta:
        verbose_name_plural = 'Фото курьера'
        verbose_name = 'Корзина курьера'