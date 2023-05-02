# from importlib.resources import _

from django import forms
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _

from .models import IssuanceAccounting
from django.forms import ModelForm


class AddIssue(forms.ModelForm):
    class Meta:
        model = IssuanceAccounting
        # fields = []
        exclude = ['user', 'slug', 'date', ]


class AddIssue_no_model(forms.Form):
    product_name = forms.CharField(max_length=100, label='Учета выдачи')
    issue_code = forms.CharField(max_length=100, label='Код выдачи')
    brand_code = forms.CharField(max_length=100, label='Код марки')
    # date = forms.DateField(dd=True)
    organization_name = forms.CharField(max_length=100, label='Наименование организации')

    field_order = ['organization_name', 'product_name', 'issue_code', 'brand_code']


class AddDetailInfo(forms.Form):
    def __init__(self, number=1, *args, **kwargs):
        super(AddDetailInfo, self).__init__(*args, **kwargs)
        self.fields[f'car_number_{number}'] = forms.CharField(label='Номер машины', max_length=15)
        self.fields[f'car_model_{number}'] = forms.CharField(label='Модель машины', max_length=15)
        self.fields[f'waybill_number_{number}'] = forms.IntegerField(label='Номер путевого листа', min_value=0)
        self.fields[f'deliver_full_name_{number}'] = forms.CharField(label='ФИО водителя', max_length=150)
        self.fields[f'deliver_number_{number}'] = forms.IntegerField(label='Табельный номер водителя', min_value=0)
        self.fields[f'issued_by_{number}'] = forms.IntegerField(label='Сколько выдано', min_value=0)

        # pass

    # def clean_issued_by(self):
    #     issued_by = self.cleaned_data['issued_by']
    #
    #     if issued_by < 0:
    #         raise ValidationError(_('Invalid range'))
    #
    #     return issued_by
