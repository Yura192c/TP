from django.contrib import admin
from .models import DetailInfo, IssuanceAccounting, DeliverDetail, CostAccountingBalances, Commision
# from document import models


# Register your models here.

@admin.register(DetailInfo)
class DetailInfoAdmin(admin.ModelAdmin):
    list_display = ('car_numder', 'car_model', 'waybill_number', 'deliver_full_name', 'deliver_number', 'is_recept',
                    'issuance_accounting',)
    list_filter = ('car_numder', 'car_model', 'waybill_number', 'deliver_full_name', 'deliver_number', 'is_recept',
                   'issuance_accounting',)
    search_fields = ('car_numder', 'car_model', 'waybill_number', 'deliver_full_name', 'deliver_number', 'is_recept',
                     'issuance_accounting',)
    empty_value_display = '-пусто-'


@admin.register(IssuanceAccounting)
class IssuanceAccountingAdmin(admin.ModelAdmin):
    list_display = ('user', 'product_name', 'issue_code', 'brand_code', 'date', 'organization_name', 'slug')
    list_filter = ('user', 'product_name', 'issue_code', 'brand_code', 'date', 'organization_name',)
    search_fields = ('user', 'product_name', 'issue_code', 'brand_code', 'date', 'organization_name',)
    empty_value_display = '-пусто-'

    prepopulated_fields = {'slug': ('id', 'user', 'issue_code', 'product_name')}


@admin.register(DeliverDetail)
class DeliverDetailAdmin(admin.ModelAdmin):
    list_display = ('cost', 'brand_of_equipment', 'garage_number', 'body_number', 'full_name', 'speedometer_reading')
    list_filter = ('cost', 'brand_of_equipment', 'garage_number', 'body_number', 'full_name', 'speedometer_reading')
    search_fields = ('brand_of_equipment', 'garage_number', 'body_number', 'full_name', 'speedometer_reading')
    empty_value_display = '-пусто-'


@admin.register(CostAccountingBalances)
class CostAccountingBalancesAdmin(admin.ModelAdmin):
    list_display = ('user', 'date', 'time', 'slug',)
    list_filter = ('user',)
    search_fields = ('user', 'deliver', 'date',)
    empty_value_display = '-пусто-'

    # prepopulated_fields = {'slug': ('user', 'time',)}

@admin.register(Commision)
class CommisionAdmin(admin.ModelAdmin):
    list_display = ('full_name', 'position', 'cost')
    list_filter = ('full_name', 'position', 'cost')