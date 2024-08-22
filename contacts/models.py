from django.db import models

class Contacts(models.Model):
    city=models.ForeignKey('mainapp.City', on_delete=models.SET_NULL, verbose_name='Контакты для города', null=True)
    iframe=models.CharField(max_length=255,verbose_name='Ссылка Яндекс Карты', help_text='Ссылка на карту Яндекс Карты с адресом (для контактов)', blank=True)
    togiz=models.CharField(max_length=255,verbose_name='Ссылка 2gis.kz',help_text='Ссылка на карту 2gis.kz с адресом (для футера)', blank=True)
    adress=models.CharField(verbose_name='Адрес',max_length=255, help_text='Без города: Мәңгілік Ел проспект, 45', blank=True)
    work_time=models.CharField(verbose_name='Время работы',max_length=255, blank=True)
    phone=models.CharField(max_length=255,verbose_name='Телефон', blank=True)
    email=models.CharField(verbose_name='Email',max_length=255, blank=True)
    whatsApp=models.CharField(verbose_name='WhatsApp',max_length=255, blank=True)
    instagram=models.CharField(verbose_name='Instagram',max_length=255, blank=True)
    def __str__(self):
        return f'Контакты для города {self.city}'
    class Meta:
        verbose_name_plural='Контакты'
        verbose_name='Контакты'
