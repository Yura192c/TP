from django.test import TestCase
from document.forms import AddIssueForm, EditIssueForm, AddDetailInfoForm, EditDetailInfoForm
from document.models import IssuanceAccounting, DetailInfo, CostAccountingBalances, DeliverDetail
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
