from django.test import TestCase
from django.urls import resolve
from document.models import IssuanceAccounting, CostAccountingBalances, DetailInfo, DeliverDetail
from account.models import CustomUser


class IssuanceAccountingModelTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        # Set up non-modified objects used by all test methods
        CustomUser.objects.create(username='testuser', password='12345')
        IssuanceAccounting.objects.create(user=CustomUser.objects.get(id=1),
                                          product_name='test',
                                          issue_code='test_issue_code',
                                          brand_code='test_brand_code',
                                          organization_name='test_organization_name',
                                          slug='test_slug'
                                          )

    def test_user_label(self):
        issuance_accounting = IssuanceAccounting.objects.get(id=1)
        field_label = issuance_accounting._meta.get_field('user').verbose_name
        self.assertEquals(field_label, 'user')

    def test_product_name_label(self):
        issuance_accounting = IssuanceAccounting.objects.get(id=1)
        field_label = issuance_accounting._meta.get_field('product_name').verbose_name
        self.assertEquals(field_label, 'Учета выдачи')

    def test_issue_code_label(self):
        issuance_accounting = IssuanceAccounting.objects.get(id=1)
        field_label = issuance_accounting._meta.get_field('issue_code').verbose_name
        self.assertEquals(field_label, 'Код выдачи')

    def test_brand_code_label(self):
        issuance_accounting = IssuanceAccounting.objects.get(id=1)
        field_label = issuance_accounting._meta.get_field('brand_code').verbose_name
        self.assertEquals(field_label, 'Код марки')

    def test_date_label(self):
        issuance_accounting = IssuanceAccounting.objects.get(id=1)
        field_label = issuance_accounting._meta.get_field('date').verbose_name
        self.assertEquals(field_label, 'Дата выдачи')

    def test_organization_name_label(self):
        issuance_accounting = IssuanceAccounting.objects.get(id=1)
        field_label = issuance_accounting._meta.get_field('organization_name').verbose_name
        self.assertEquals(field_label, 'organization name')

    def test_object_str(self):
        issuance_accounting = IssuanceAccounting.objects.get(id=1)
        expected_object_name = f'{issuance_accounting.organization_name}'
        self.assertEquals(expected_object_name, str(issuance_accounting))

    def test_get_absolute_url(self):
        issuance_accounting = IssuanceAccounting.objects.get(id=1)
        # This will also fail if the urlconf is not defined.
        self.assertEquals(issuance_accounting.get_absolute_url(), '/document/issuance/test_slug')


class DetailInfoModelTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        # Set up non-modified objects used by all test methods
        CustomUser.objects.create(username='testuser', password='12345')
        IssuanceAccounting.objects.create(user=CustomUser.objects.get(id=1),
                                          product_name='test',
                                          issue_code='test_issue_code',
                                          brand_code='test_brand_code',
                                          organization_name='test_organization_name',
                                          slug='test_slug'
                                          )
        DetailInfo.objects.create(car_numder='test_car_numder',
                                  car_model='test_car_model',
                                  waybill_number=4343443,
                                  deliver_full_name='test_deliver_full_name',
                                  deliver_number=1222331,
                                  issued_by=12000,
                                  is_recept=True,
                                  issuance_accounting=IssuanceAccounting.objects.get(id=1)
                                  )

    def test_car_numder_label(self):
        detail_info = DetailInfo.objects.get(id=1)
        field_label = detail_info._meta.get_field('car_numder').verbose_name
        self.assertEquals(field_label, 'Номер машины')

    def test_car_model_label(self):
        detail_info = DetailInfo.objects.get(id=1)
        field_label = detail_info._meta.get_field('car_model').verbose_name
        self.assertEquals(field_label, 'Модель машины')

    def test_waybill_number_label(self):
        detail_info = DetailInfo.objects.get(id=1)
        field_label = detail_info._meta.get_field('waybill_number').verbose_name
        self.assertEquals(field_label, 'Номер путевого листа')

    def test_deliver_full_name_label(self):
        detail_info = DetailInfo.objects.get(id=1)
        field_label = detail_info._meta.get_field('deliver_full_name').verbose_name
        self.assertEquals(field_label, 'ФИО водителя')

    def test_deliver_number_label(self):
        detail_info = DetailInfo.objects.get(id=1)
        field_label = detail_info._meta.get_field('deliver_number').verbose_name
        self.assertEquals(field_label, 'Табельный номер водителя')

    def test_issued_by_label(self):
        detail_info = DetailInfo.objects.get(id=1)
        field_label = detail_info._meta.get_field('issued_by').verbose_name
        self.assertEquals(field_label, 'Сколько выдано')

    def test_is_recept_label(self):
        detail_info = DetailInfo.objects.get(id=1)
        field_label = detail_info._meta.get_field('is_recept').verbose_name
        self.assertEquals(field_label, 'Статус получения')

    def test_issuance_accounting_label(self):
        detail_info = DetailInfo.objects.get(id=1)
        field_label = detail_info._meta.get_field('issuance_accounting').verbose_name
        self.assertEquals(field_label, 'Выдача ГСМ')

    def test_object_str(self):
        detail_info = DetailInfo.objects.get(id=1)
        expected_object_name = f'{detail_info.car_numder}'
        self.assertEquals(expected_object_name, str(detail_info))


class CostAccountingBalancesModelTest(TestCase):
    # @classmethod
    # def setUpTestData(cls):
    #     # Set up non-modified objects used by all test methods
    #     CustomUser.objects.create(username='testuser', password='12345')
    #     CostAccountingBalances.objects.create(user=CustomUser.objects.get(id=1),
    #                                       product_name='test',
    #                                       issue_code='test_issue_code',
    #                                       brand_code='test_brand_code',
    #                                       organization_name='test_organization_name',
    #                                       slug='test_slug'
    #                                       )
    pass


class DeliverDetailModelTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        # Set up non-modified objects used by all test methods
        CustomUser.objects.create(username='testuser', password='12345')
        CostAccountingBalances.objects.create(user=CustomUser.objects.get(id=1))


        deliver_detail = DeliverDetail.objects.create(brand_of_equipment='test_brand_of_equipment',
                                                      garage_number='test_garage_number',
                                                      body_number='test_body_number',
                                                      full_name='test_full_name',
                                                      speedometer_reading=333333,
                                                      fuel_brand='test_fuel_brand',
                                                      remaining_fuel=333333,
                                                      cost=CostAccountingBalances.objects.get(id=1))

    def test_brand_of_equipment_label(self):
        deliver_detail = DeliverDetail.objects.get(id=1)
        field_label = deliver_detail._meta.get_field('brand_of_equipment').verbose_name
        self.assertEquals(field_label, 'Марка технического средства')

    def test_garage_number_label(self):
        deliver_detail = DeliverDetail.objects.get(id=1)
        field_label = deliver_detail._meta.get_field('garage_number').verbose_name
        self.assertEquals(field_label, 'Гаражный(гос.) номер')

    def test_body_number_label(self):
        deliver_detail = DeliverDetail.objects.get(id=1)
        field_label = deliver_detail._meta.get_field('body_number').verbose_name
        self.assertEquals(field_label, 'Номер кузова')

    def test_full_name_label(self):
        deliver_detail = DeliverDetail.objects.get(id=1)
        field_label = deliver_detail._meta.get_field('full_name').verbose_name
        self.assertEquals(field_label, 'ФИО водителя')

    def test_speedometer_reading_label(self):
        deliver_detail = DeliverDetail.objects.get(id=1)
        field_label = deliver_detail._meta.get_field('speedometer_reading').verbose_name
        self.assertEquals(field_label, 'Показания спидометра')

    def test_fuel_brand_label(self):
        deliver_detail = DeliverDetail.objects.get(id=1)
        field_label = deliver_detail._meta.get_field('fuel_brand').verbose_name
        self.assertEquals(field_label, 'Марка топлива')

    def test_remaining_fuel_label(self):
        deliver_detail = DeliverDetail.objects.get(id=1)
        field_label = deliver_detail._meta.get_field('remaining_fuel').verbose_name
        self.assertEquals(field_label, 'Остаток топлива')

    def test_cost_label(self):
        deliver_detail = DeliverDetail.objects.get(id=1)
        field_label = deliver_detail._meta.get_field('cost').verbose_name
        self.assertEquals(field_label, 'Учет расходов')

    def test_object_str(self):
        deliver_detail = DeliverDetail.objects.get(id=1)
        expected_object_name = f'{deliver_detail.full_name}'
        self.assertEquals(expected_object_name, str(deliver_detail))