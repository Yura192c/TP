from django.db import models
from django.utils.text import slugify

from account.models import CustomUser
from django.urls import reverse


# Create your models here.


class IssuanceAccounting(models.Model):
    '''
    Выдача ГСМ
    '''
    ''' Номер - id
    Ответственный - user
    табельный номер - user.id
    '''
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)  # Материально ответсвенное лицо
    product_name = models.CharField('Учета выдачи', max_length=100)
    issue_code = models.CharField('Код выдачи', max_length=100)
    brand_code = models.CharField('Код марки', max_length=100)
    date = models.DateField('Дата выдачи', auto_now_add=True)
    organization_name = models.CharField(max_length=100)
    slug = models.SlugField(max_length=200, db_index=True, unique=True)

    def __str__(self):
        return self.organization_name

    # def save(self, *args, **kwargs):
    #
    #     self.slug = slugify(f'{kwargs["issue_code"]} {kwargs["product_name"]} {kwargs["brand_code"]}')
    #     super(IssuanceAccounting, self).save(*args, **kwargs)

    class Meta:
        verbose_name = 'Выдача материалов'
        verbose_name_plural = 'Выдача материалов'

    def get_absolute_url(self):
        # return reverse('document:document', kwargs={'pk': self.pk})
        return reverse('document_info',
                       args=[self.slug])


class DetailInfo(models.Model):
    """
    Информация о водителе в выдаче ГСМ
    """
    car_numder = models.CharField('Номер машины', max_length=15)
    car_model = models.CharField('Модель машины', max_length=15)
    waybill_number = models.PositiveIntegerField('Номер путевого листа')
    deliver_full_name = models.CharField('ФИО водителя', max_length=150)
    deliver_number = models.PositiveIntegerField('Табельный номер водителя')
    issued_by = models.PositiveIntegerField('Сколько выдано', default=0)
    is_recept = models.BooleanField('Статус получения', default=True)
    issuance_accounting = models.ForeignKey(IssuanceAccounting, verbose_name='Выдача ГСМ', on_delete=models.CASCADE,
                                            null=True)

    def __str__(self):
        return self.car_numder

    class Meta:
        verbose_name = 'Детальная информация'
        verbose_name_plural = 'Детальная информация'


class CostAccountingBalances(models.Model):
    '''
    Расход ГСМ
    '''
    date = models.DateField('Дата выдачи', auto_now_add=True, null=True)
    time = models.TimeField('Время выдачи', auto_now_add=True, null=True)
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    slug = models.SlugField(max_length=200, db_index=True, unique=True)

    class Meta:
        verbose_name = 'Сальдо по учету расходов'
        verbose_name_plural = 'Сальдо по учету расходов'

    def __str__(self):
        return f'{self.id}//{self.date}//{self.user}'

    def get_absolute_url(self):
        return reverse('cost_info',
                       args=[self.slug])
    
    # def save(self, *args, **kwargs):
    
    #     self.slug = slugify(f'{kwargs["user"]} {kwargs["date"]} {kwargs["id"]}')
    #     super(CostAccountingBalances, self).save(*args, **kwargs)


class DeliverDetail(models.Model):
    brand_of_equipment = models.CharField('Марка технического средства', max_length=100)
    garage_number = models.CharField('Гаражный(гос.) номер', max_length=100)
    body_number = models.CharField('Номер кузова', max_length=100)
    full_name = models.CharField('ФИО водителя', max_length=100)
    speedometer_reading = models.PositiveIntegerField('Показания спидометра')
    fuel_brand = models.CharField('Марка топлива', max_length=100)
    remaining_fuel = models.PositiveIntegerField('Остаток топлива')
    cost = models.ForeignKey(CostAccountingBalances, verbose_name='Учет расходов', on_delete=models.CASCADE,
                             null=True)

    class Meta:
        verbose_name = 'Информация о водителе'
        verbose_name_plural = 'Информация о водителе'

    def __str__(self):
        return self.full_name


class Commision(models.Model):
    '''
    Комиссия в составе выдачи ГСМ
    '''
    position = models.CharField('Должность', max_length=100)
    full_name = models.CharField('ФИО', max_length=200)
    cost = models.ForeignKey(CostAccountingBalances, verbose_name='Учет расходов', on_delete=models.CASCADE,
                             null=True)

    class Meta:
        verbose_name = 'Комиссия выдачи'
        verbose_name_plural = 'Комиссия выдачи'

    # def get_absolute_url(self):
    #     return reverse('commision_info',
    #                    args=[self.slug])