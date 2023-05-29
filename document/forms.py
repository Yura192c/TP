# from importlib.resources import _

from django import forms
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _

from .models import IssuanceAccounting
from django.forms import ModelForm


class AddIssueForm(forms.Form):
    organization_name = forms.CharField(max_length=100, label='Наименование организации')
    product_name = forms.CharField(max_length=100, label='Учета выдачи')
    issue_code = forms.CharField(max_length=100, label='Код выдачи')
    brand_code = forms.CharField(max_length=100, label='Код марки')
    # date = forms.DateField(dd=True)

    field_order = ['organization_name', 'product_name', 'issue_code', 'brand_code']


class EditIssueForm(forms.Form):
    def __init__(self, issuance_accounting_model=None, *args, **kwargs):
        super(EditIssueForm, self).__init__(*args, **kwargs)
        self.fields['organization_name'] = forms.CharField(max_length=100, label='Наименование организации',
                                                           initial=issuance_accounting_model.organization_name)
        self.fields['product_name'] = forms.CharField(max_length=100, label='Учета выдачи',
                                                      initial=issuance_accounting_model.product_name)
        self.fields['issue_code'] = forms.CharField(max_length=100, label='Код выдачи',
                                                    initial=issuance_accounting_model.issue_code)
        self.fields['brand_code'] = forms.CharField(max_length=100, label='Код марки',
                                                    initial=issuance_accounting_model.brand_code)
        # date = forms.DateField(dd=True)

        # field_order = ['organization_name', 'product_name', 'issue_code', 'brand_code']


class AddDetailInfoForm(forms.Form):
    def __init__(self, number=1, *args, **kwargs):
        super(AddDetailInfoForm, self).__init__(*args, **kwargs)
        self.fields[f'car_number_{number}'] = forms.CharField(label='Номер машины', max_length=15)
        self.fields[f'car_model_{number}'] = forms.CharField(label='Модель машины', max_length=15)
        self.fields[f'waybill_number_{number}'] = forms.IntegerField(label='Номер путевого листа', min_value=0)
        self.fields[f'deliver_full_name_{number}'] = forms.CharField(label='ФИО водителя', max_length=150)
        self.fields[f'deliver_number_{number}'] = forms.IntegerField(label='Табельный номер водителя', min_value=0)
        self.fields[f'issued_by_{number}'] = forms.IntegerField(label='Сколько выдано', min_value=0)


class EditDetailInfoForm(forms.Form):
    def __init__(self, DetailInfoModel=None, number=1, *args, **kwargs):
        super(EditDetailInfoForm, self).__init__(*args, **kwargs)
        self.fields[f'car_number_{number}'] = forms.CharField(label='Номер машины', max_length=15,
                                                              initial=DetailInfoModel.car_numder)
        self.fields[f'car_model_{number}'] = forms.CharField(label='Модель машины', max_length=15,
                                                             initial=DetailInfoModel.car_model)
        self.fields[f'waybill_number_{number}'] = forms.IntegerField(label='Номер путевого листа', min_value=0,
                                                                     initial=DetailInfoModel.waybill_number)
        self.fields[f'deliver_full_name_{number}'] = forms.CharField(label='ФИО водителя', max_length=150,
                                                                     initial=DetailInfoModel.deliver_full_name)
        self.fields[f'deliver_number_{number}'] = forms.IntegerField(label='Табельный номер водителя', min_value=0,
                                                                     initial=DetailInfoModel.deliver_number)
        self.fields[f'issued_by_{number}'] = forms.IntegerField(label='Сколько выдано', min_value=0,
                                                                initial=DetailInfoModel.issued_by)

        # pass

    # def clean_issued_by(self):
    #     issued_by = self.cleaned_data['issued_by']
    #
    #     if issued_by < 0:
    #         raise ValidationError(_('Invalid range'))
    #
    #     return issued_by


class AddCostAccountingBalancesForm(forms.Form):
    pass


class AddDeliverDetailForm(forms.Form):
    """ Форма для добавления детальной информации о выдаче ГСМ"""

    def __init__(self, number=1, *args, **kwargs):
        super(AddDeliverDetailForm, self).__init__(*args, **kwargs)
        self.fields[f'brand_of_equipment_{number}'] = forms.CharField(label='Марка технического средства', max_length=100)
        self.fields[f'garage_number_{number}'] = forms.CharField(label='Гаражный(гос.) номер', max_length=100)
        self.fields[f'body_number_{number}'] = forms.CharField(label='Номер кузова', max_length=100)
        self.fields[f'full_name_{number}'] = forms.CharField(label='ФИО водителя', max_length=100)
        self.fields[f'speedometer_reading_{number}'] = forms.IntegerField(label='Показания спидометра', min_value=0)
        self.fields[f'fuel_brand_{number}'] = forms.CharField(label='Марка топлива', max_length=100)
        self.fields[f'remaining_fuel_{number}'] = forms.IntegerField(label='Остаток топлива', min_value=0)


class AddCommisionForm(forms.Form):
    """ Форма для добавления состава комиссии учета выдачи ГСМ"""
    def __init__(self, number=1, *args, **kwargs):
        super(AddCommisionForm, self).__init__(*args, **kwargs)
        self.fields[f'position_{number}'] = forms.CharField(label='Должность', max_length=100)
        self.fields[f'com_full_name_{number}'] = forms.CharField(label='ФИО', max_length=200)
    # position = forms.CharField(label='Должность', max_length=100)
    # com_full_name = forms.CharField(label='ФИО', max_length=200)


class EditCommisionForm(forms.Form):
    """ Форма для редактирования состава комиссии учета выдачи ГСМ """

    def __init__(self, CommisionModel=None, number=1, *args, **kwargs):
        super(EditCommisionForm, self).__init__(*args, **kwargs)
        self.fields[f'position_{number}'] = forms.CharField(label='Должность', max_length=100,
                                                            initial=CommisionModel.position)
        self.fields[f'com_full_name_{number}'] = forms.CharField(label='ФИО', max_length=200,
                                                             initial=CommisionModel.full_name)


class EditDeliverDetailForm(forms.Form):
    """ Форма редактирвония информации о водителях в выдаче ГСМ """

    def __init__(self, DeliverDetailModel=None, number=1, *args, **kwargs):
        super(EditDeliverDetailForm, self).__init__(*args, **kwargs)
        self.fields[f'brand_of_equipment_{number}'] = forms.CharField(label='Марка технического средства',
                                                                      max_length=100,
                                                                      initial=DeliverDetailModel.brand_of_equipment)
        self.fields[f'garage_number_{number}'] = forms.CharField(label='Гаражный(гос.) номер', max_length=100,
                                                                 initial=DeliverDetailModel.garage_number)
        self.fields[f'body_number_{number}'] = forms.CharField(label='Номер кузова', max_length=100,
                                                               initial=DeliverDetailModel.body_number)
        self.fields[f'full_name_{number}'] = forms.CharField(label='ФИО водителя', max_length=100,
                                                             initial=DeliverDetailModel.full_name)
        self.fields[f'speedometer_reading_{number}'] = forms.IntegerField(label='Показания спидометра', min_value=0,
                                                                          initial=DeliverDetailModel.speedometer_reading)
        self.fields[f'fuel_brand_{number}'] = forms.CharField(label='Марка топлива', max_length=100,
                                                              initial=DeliverDetailModel.fuel_brand)
        self.fields[f'remaining_fuel_{number}'] = forms.IntegerField(label='Остаток топлива', min_value=0,
                                                                     initial=DeliverDetailModel.remaining_fuel)
