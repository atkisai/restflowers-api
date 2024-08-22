from django.db import models

class Order(models.Model):
    email = models.CharField('Почта',max_length=255)
    fio = models.CharField('ФИО',max_length=255)
    phone = models.CharField('Телефон',max_length=255)
    city = models.CharField('Город проживания',max_length=255)
    city_fr = models.CharField('В каком городе открыть',max_length=255, null=True)
    brend = models.CharField('Бренд',max_length=255)
    kapital = models.CharField('Капитал',max_length=255)
    opit = models.CharField('Опыт в предпринимательстве',max_length=255)
    obopite = models.TextField('Опыт в бинессе')
    velbiznes = models.CharField('Скем вел бизнесс',max_length=255)
    pochemu = models.TextField('Почему хотите приобрести')
    date_add = models.DateTimeField('Дата добавление', auto_now_add=True)
   
    def __str__(self):
        return f'Заявка {self.fio}'
   
    class Meta:
        verbose_name_plural = 'Заявки'
        verbose_name = 'Заявка'
        ordering=['-date_add']
