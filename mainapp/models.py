import email
from django.contrib.auth.models import User
from django.db import models
from django.urls import reverse


class Filial(models.Model):
    name = models.CharField('Филиал', max_length=255)
    post = models.CharField('Почта', max_length=255, blank=True, null=True)
    # city = models.ForeignKey('City', on_delete=models.SET_NULL, verbose_name='Город', blank=True, null=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = 'Филиалы'
        verbose_name = 'Филиал'


class Users(models.Model):
    choices = (('Клиент', 'Клиент'), ('Админ', 'Админ'))
    user = models.OneToOneField(User, on_delete=models.CASCADE, verbose_name='Пользователь')
    name = models.CharField('Имя', max_length=255, blank=True,null=True)
    phone = models.CharField('Телефон', max_length=255, blank=True,null=True)
    email = models.CharField('Почта', max_length=255, blank=True,null=True)
    work = models.CharField('Должность', max_length=255,choices=choices, default='Родитель')
    city = models.ForeignKey('City', on_delete=models.SET_NULL, blank=True, null=True, verbose_name='Город', help_text='Для админа укажите его город')
    filial = models.ForeignKey('Filial', on_delete=models.SET_NULL, verbose_name='Филиал', blank=True, null=True)

    def __str__(self):
        return f'{self.user.username} {self.work}'

    def full_name(self):
        return f'{self.user.first_name} {self.user.last_name}'

    class Meta:
        verbose_name = 'Пользователи'
        verbose_name_plural = 'Пользователи'


class Category(models.Model):
    name = models.CharField('Название', max_length=255,help_text='Введите название')
    
    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = 'Категория'
        verbose_name = 'Категория'


class Povods(models.Model):
    name = models.CharField('Название', max_length=255,help_text='Введите название')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = 'Поводы'
        verbose_name = 'Поводы'


class Counts_Flowers(models.Model):
    count_in = models.PositiveIntegerField('Количество')

    def __str__(self):
        return f'{self.count_in}'

    class Meta:
        verbose_name_plural = 'Количество'
        verbose_name = 'Количество'


class City(models.Model):
    name = models.CharField('Город', max_length=255, help_text='Введите город')
    url_name = models.CharField('URL', max_length=255, help_text='Название города в строке браузера (без /)', null=True)
    keywords = models.CharField('CEO-описание', max_length=255, help_text='Введите текст', null=True, blank=True)
    description = models.CharField('CEO-ключевые слова', max_length=255, help_text='Ключевые слова через запятую', null=True, blank=True)
    post = models.CharField('Почта', max_length=255, blank=True, null=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = 'Города'
        verbose_name = 'Город'


class Flowers(models.Model):
    name = models.CharField('Название', max_length=255,help_text='Введите название')
    description = models.TextField('Описание', help_text='Введите описание',blank=True)
    price = models.PositiveIntegerField('Цена')
    category = models.ManyToManyField(Category, related_name='category_flowers', verbose_name='Категория')
    povod = models.ManyToManyField(Povods, related_name='povods_flowers', verbose_name='Поводы')
    count_in = models.ForeignKey(Counts_Flowers, verbose_name='Количество', on_delete=models.CASCADE)
    ready = models.BooleanField('Готовый букет', default=False)
    comp = models.BooleanField('Композиции', default=False)
    enable = models.BooleanField('Активный', default=True)
    valentine = models.BooleanField('8 март', default=False)
    stock = models.BooleanField('Акция', default=False, help_text='При активации акции не забудьте указать процент скидки.')
    start_stock = models.DateField('Старт акции', blank=True, null=True, help_text='Дату старта и конца акции можно не указывать.')
    end_stock = models.DateField('Конец акции', blank=True, null=True)
    percent_stock = models.PositiveIntegerField(verbose_name='Процент скидки')
    date_time = models.DateTimeField(auto_now_add=True, verbose_name='Дата добавления')
    city = models.ManyToManyField(City, related_name='city_flowers', verbose_name='Города')
    filial = models.ForeignKey('Filial', on_delete=models.SET_NULL, verbose_name='Филиал', blank=True, null=True)
    set = models.ForeignKey('SetsExtraProducts', on_delete=models.SET_NULL, verbose_name='Сет допов', null=True, default=2)
    col = models.PositiveIntegerField('техническое поле, не трогать', default=1)
    total = models.PositiveIntegerField('техническое поле, не трогать', default=0)
    @property
    def price_stock(self):
        price=self.price-(self.price/100*self.percent_stock)
        return f"{price:.{0}f}"
    @property
    def total_price(self):
        if self.stock==True:
            price=self.price-(self.price/100*self.percent_stock)
            return f"{price:.{0}f}"
        else:
            return self.price
    
    # @property
    # def images(self):
    #     flower = (x for x in Flowers.objects if x.images())
    #     return flower.images.all()

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = 'Цветы'
        verbose_name = 'Цветы'
        ordering = ['-date_time']

    def get_absolute_url(self):
        return reverse('flower_detail', args=[self.id])


class FlowerImages(models.Model):
    flower = models.ForeignKey(Flowers, on_delete=models.CASCADE, verbose_name='Цветы', related_name='images')
    image = models.ImageField(upload_to='flower/', verbose_name='Картина')

    def __str__(self):
        return f'Картина {self.flower}'

    class Meta:
        verbose_name_plural = 'Картины'
        verbose_name = 'Картины'


class ExtraProducts(models.Model):
    name = models.CharField('Название', max_length=255,help_text='Введите название')
    price = models.PositiveIntegerField('Цена')
    picture = models.ImageField(upload_to='extraproducts/', verbose_name='Картина', default='')
    col = models.PositiveIntegerField('техническое поле, не трогать', default=1)
    selected = models.BooleanField('техническое поле, не трогать',default=False)
    total = models.PositiveIntegerField('техническое поле, не трогать',null=True, blank=True)

    def __str__(self):
        return f'{self.name}'

    class Meta:
        verbose_name_plural = 'Допы'
        verbose_name = 'Допы'


class SetsExtraProducts(models.Model):
    name = models.CharField('Название', max_length=255,help_text='Введите название')
    extra = models.ManyToManyField(ExtraProducts,related_name='extra_poducts',verbose_name='Доп')

    def __str__(self):
        return f'{self.name}'

    class Meta:
        verbose_name_plural = 'Допы Сеты'
        verbose_name = 'Допы Сеты'



# class Cart(models.Model):
#     name = models.CharField(max_length=255)

#     def __str__(self):
#         return self.name


# class CartExtra(models.Model):
#     extra = models.ForeignKey(ExtraProducts, on_delete=models.CASCADE)
#     flower = models.ForeignKey(Flowers, on_delete=models.CASCADE)
#     quantity = models.PositiveIntegerField()
#     cart = models.PositiveIntegerField()
#     cart_in = models.ForeignKey('Cart', on_delete=models.CASCADE, default=1)

#     def __str__(self):
#         return f'Корзина экстра продукты {self.id}'

#     class Meta:
#         verbose_name_plural = 'Корзина экстра продукта'
#         verbose_name = 'Корзина экстра продукта'


# class CartProduct(models.Model):
#     flower = models.ForeignKey(Flowers, on_delete=models.CASCADE)
#     cart = models.ForeignKey('Cart', on_delete=models.CASCADE, default=None)
#     quantity = models.PositiveIntegerField(default=1)
#     total = models.PositiveIntegerField()

#     def __str__(self):
#         return f'Корзина продукты {self.id}'

#     class Meta:
#         verbose_name_plural = 'Корзина продукта'
#         verbose_name = 'Корзина продукта'


# class TextDescription(models.Model):
#     city=models.ForeignKey('mainapp.City', on_delete=models.SET_NULL, verbose_name='Для города', null=True)
#     description = models.ManyToManyField('TextContent', related_name='content_description' ,verbose_name='Контент вопросов')

#     def __str__(self):
#         return f'Блок вопросов для города {self.city}'

#     class Meta:
#         verbose_name_plural = 'Блок вопросов'
#         verbose_name = 'Блок вопросов'


# class TextContent(models.Model):
#     title = models.CharField('Вопрос', max_length=255, help_text='Введите вопрос')
#     text = models.TextField('Ответ', help_text='Введите ответ', null=True)

#     def __str__(self):
#         return self.title

#     class Meta:
#         verbose_name_plural = 'Контент вопросов'
#         verbose_name = 'Контент вопросов'


# class TextName(models.Model):
#     name = models.CharField('Название', max_length=255)

#     def __str__(self):
#         return f'Название'

#     class Meta:
#         verbose_name_plural = 'Название'
#         verbose_name = 'Название'


# class Delivery(models.Model):
#     city=models.ForeignKey('mainapp.City', on_delete=models.SET_NULL, verbose_name='Для города', null=True)
#     price = models.PositiveIntegerField('Стоимость доставки', null=True)
#     delivery_city = models.TextField('Стоимость доставки по городу:', null=True, blank=True)
#     delivery_regions = models.TextField('Стоимость доставки в регионы:', null=True, blank=True)
#     delivery_time = models.TextField('Время доставки:', null=True, blank=True)

#     def __str__(self):
#         return f'Доставка для города {self.city}'

#     class Meta:
#         verbose_name_plural = 'Доставка'
#         verbose_name = 'Доставка'