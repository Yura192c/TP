from django.test import TestCase
from document.forms import AddIssueForm, EditIssueForm, AddDetailInfoForm, EditDetailInfoForm, AddDeliverDetailForm, \
    AddCommisionForm, EditCommisionForm, EditDeliverDetailForm
from document.models import IssuanceAccounting, DetailInfo, CostAccountingBalances, DeliverDetail, \
    Commision
from account.models import CustomUser


class AddIssueFormTest(TestCase):

    def test_form_has_fields(self):
        form = AddIssueForm()
        expected = ['organization_name', 'product_name', 'issue_code', 'brand_code']
        actual = list(form.fields)
        self.assertSequenceEqual(expected, actual)


class EditIssueFormTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        CustomUser.objects.create(username='testuser', password='12345')
        IssuanceAccounting.objects.create(user=CustomUser.objects.get(id=1),
                                          product_name='test',
                                          issue_code='test_issue_code',
                                          brand_code='test_brand_code',
                                          organization_name='test_organization_name',
                                          slug='test_slug'
                                          )

    def test_form_has_fields(self):
        form = EditIssueForm(IssuanceAccounting.objects.get(id=1))
        expected = ['organization_name', 'product_name', 'issue_code', 'brand_code']
        actual = list(form.fields)
        self.assertSequenceEqual(expected, actual)

    def test_form_correct_data_in_fields(self):
        form = EditIssueForm(IssuanceAccounting.objects.get(id=1))
        expected = ['test_organization_name', 'test', 'test_issue_code', 'test_brand_code']
        actual = [form['organization_name'].value(),
                  form['product_name'].value(),
                  form['issue_code'].value(),
                  form['brand_code'].value()]
        self.assertSequenceEqual(expected, actual)


class AddDetailInfoFormTest(TestCase):

    def test_form_has_fields(self):
        form = AddDetailInfoForm(1)
        expected = ['car_number_1', 'car_model_1', 'waybill_number_1', 'deliver_full_name_1', 'deliver_number_1',
                    'issued_by_1', ]
        actual = list(form.fields)
        self.assertSequenceEqual(expected, actual)


class EditDetailInfoFormTest(TestCase):

    @classmethod
    def setUpTestData(cls):
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

    def test_form_has_fields(self):
        form = EditDetailInfoForm(DetailInfo.objects.get(id=1), 1)
        expected = ['car_number_1', 'car_model_1', 'waybill_number_1', 'deliver_full_name_1', 'deliver_number_1',
                    'issued_by_1', ]
        actual = list(form.fields)
        self.assertSequenceEqual(expected, actual)

    def test_form_correct_data_in_fields(self):
        form = EditDetailInfoForm(DetailInfo.objects.get(id=1), 1)
        expected = ['test_car_numder', 'test_car_model', 4343443, 'test_deliver_full_name', 1222331, 12000]
        actual = [form['car_number_1'].value(),
                  form['car_model_1'].value(),
                  form['waybill_number_1'].value(),
                  form['deliver_full_name_1'].value(),
                  form['deliver_number_1'].value(),
                  form['issued_by_1'].value()]
        self.assertSequenceEqual(expected, actual)


class AddDeliverDetailFormTest(TestCase):

    def test_form_has_fields(self):
        form = AddDeliverDetailForm(1)
        expected = ['brand_of_equipment_1', 'garage_number_1', 'body_number_1', 'full_name_1', 'speedometer_reading_1',
                    'fuel_brand_1', 'remaining_fuel_1']
        actual = list(form.fields)
        self.assertSequenceEqual(expected, actual)


class AddCommissionFormTest(TestCase):

    def test_form_has_fields(self):
        form = AddCommisionForm(1)
        expected = ['position_1', 'com_full_name_1', ]
        actual = list(form.fields)
        self.assertSequenceEqual(expected, actual)


class EditCommissionFormTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        id = CustomUser.objects.create(username='testuser', password='12345').id
        cost_id = CostAccountingBalances.objects.create(
            user=CustomUser.objects.get(id=id),
            slug='test_slug', ).id
        Commision.objects.create(position='test_position',
                                 full_name='test_com_full_name',
                                 cost=CostAccountingBalances.objects.get(id=cost_id))

    def test_form_has_fields(self):
        form = EditCommisionForm(Commision.objects.get(id=1), 1)
        expected = ['position_1', 'com_full_name_1', ]
        actual = list(form.fields)
        self.assertSequenceEqual(expected, actual)

    def test_form_correct_data_in_fields(self):
        form = EditCommisionForm(Commision.objects.get(id=1), 1)
        expected = ['test_position', 'test_com_full_name']
        actual = [form['position_1'].value(),
                  form['com_full_name_1'].value()]
        self.assertSequenceEqual(expected, actual)


class EditDeliverDetailsForm(TestCase):

    @classmethod
    def setUpTestData(cls):
        id = CustomUser.objects.create(username='testuser', password='12345').id
        cost_id = CostAccountingBalances.objects.create(
            user=CustomUser.objects.get(id=id),
            slug='test_slug', ).id
        DeliverDetail.objects.create(brand_of_equipment='test_brand_of_equipment',
                                     garage_number='test_garage_number',
                                     body_number='test_body_number',
                                     full_name='test_full_name',
                                     speedometer_reading=12345,
                                     fuel_brand='test_fuel_brand',
                                     remaining_fuel=12345,
                                     cost=CostAccountingBalances.objects.get(id=cost_id))

    def test_form_has_fields(self):
        form = EditDeliverDetailForm(DeliverDetail.objects.get(id=1), 1)
        expected = ['brand_of_equipment_1', 'garage_number_1', 'body_number_1', 'full_name_1', 'speedometer_reading_1',
                    'fuel_brand_1', 'remaining_fuel_1']
        actual = list(form.fields)
        self.assertSequenceEqual(expected, actual)

    def test_form_correct_data_in_fields(self):
        form = EditDeliverDetailForm(DeliverDetail.objects.get(id=1), 1)
        expected = ['test_brand_of_equipment', 'test_garage_number', 'test_body_number', 'test_full_name', 12345,
                    'test_fuel_brand', 12345]
        actual = [form['brand_of_equipment_1'].value(),
                  form['garage_number_1'].value(),
                  form['body_number_1'].value(),
                  form['full_name_1'].value(),
                  form['speedometer_reading_1'].value(),
                  form['fuel_brand_1'].value(),
                  form['remaining_fuel_1'].value()]
        self.assertSequenceEqual(expected, actual)


