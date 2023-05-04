from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from django.views.decorators.http import require_POST

from account.models import CustomUser
from .models import DetailInfo, IssuanceAccounting, DeliverDetail, CostAccountingBalances
from .forms import AddIssueForm, AddDetailInfoForm, EditDetailInfoForm, EditIssueForm
import datetime
import re


def create_slug(name: str) -> str:
    slug = name.lower().strip()
    slug = re.sub(r'[^\w\s-]', '', slug)
    slug = re.sub(r'[\s_-]+', '-', slug)
    slug = re.sub(r'^-+|-+$', '', slug)
    return slug


# Create your views here.

def show_documents(request):
    """
    Представление для отображения всех документов
    """
    if not request.user.is_authenticated:
        pass
        # return redirect('account:login')
    user = request.user.id
    issuance_accounting = IssuanceAccounting.objects.filter(user=user)
    cost_accounting_balances = CostAccountingBalances.objects.filter(user=user)
    return render(request,
                  'account/dashboard.html',
                  {'Issuance_Accounting': issuance_accounting,
                   'Cost_Accounting_Balances': cost_accounting_balances, })


def issuance_info(request, document_slug=None):
    """
    Представление для отображения информации о учета выдачи
    """
    issuance_accounting = get_object_or_404(IssuanceAccounting,
                                            slug=document_slug)
    detail_info = DetailInfo.objects.filter(issuance_accounting_id=issuance_accounting.id)
    cost_accounting_balances = CostAccountingBalances.objects.filter(slug=document_slug)
    return render(request,
                  'document/issuance_info.html',
                  {'Issuance_Accounting': issuance_accounting,
                   'Detail_Info': detail_info,
                   'Cost_Accounting_Balances': cost_accounting_balances, })


def cost_info(request, cost_slug=None):
    """
    Представление для отображения информации о учета выдачи
    """
    cost_accounting = get_object_or_404(CostAccountingBalances,
                                        slug=cost_slug)
    delivers = DeliverDetail.objects.filter(cost=cost_accounting)
    return render(request,
                  'document/cost_info.html',
                  {'Cost_Accounting': cost_accounting,
                   'Delivers': delivers, })


def add_issuance(request):
    """
    Добаление отчета
    """
    count = int(request.GET.get('count', 0))
    count = count + 1
    count_range = range(0, count)
    if request.method == 'POST':
        form = AddIssueForm(request.POST)
        deliver_forms = [AddDetailInfoForm(number, request.POST) for number in range(1, count + 2)]
        deliver_forms_is_valid = all(list(map(lambda dev_form: dev_form.is_valid(), deliver_forms)))
        if form.is_valid() and deliver_forms_is_valid:
            try:

                IssuanceAccounting.objects.create(
                    user=get_object_or_404(CustomUser,
                                           id=request.user.id),
                    product_name=form.cleaned_data['product_name'],
                    issue_code=form.cleaned_data['issue_code'],
                    brand_code=form.cleaned_data['brand_code'],
                    date=datetime.date.today(),
                    organization_name=form.cleaned_data['organization_name'],
                    slug=create_slug(str(str(request.user.id) + '-' +
                                         str(form.cleaned_data['issue_code'])))
                )
            except:
                pass

            for index, deliver_form in enumerate(deliver_forms, 1):
                DetailInfo.objects.create(
                    car_numder=deliver_form.cleaned_data[f'car_number_{index}'],
                    car_model=deliver_form.cleaned_data[f'car_model_{index}'],
                    waybill_number=deliver_form.cleaned_data[f'waybill_number_{index}'],
                    deliver_full_name=deliver_form.cleaned_data[f'deliver_full_name_{index}'],
                    deliver_number=deliver_form.cleaned_data[f'deliver_number_{index}'],
                    issued_by=deliver_form.cleaned_data[f'issued_by_{index}'],
                    is_recept=True,
                    issuance_accounting=get_object_or_404(IssuanceAccounting,
                                                          user=request.user.id,
                                                          product_name=form.cleaned_data['product_name'],
                                                          issue_code=form.cleaned_data['issue_code'],
                                                          brand_code=form.cleaned_data['brand_code'],
                                                          )
                )

            return redirect('show_documents')
    else:
        form = AddIssueForm()
        # deliver_form = AddDetailInfo()
        deliver_forms = [AddDetailInfoForm(number) for number in range(1, count + 1)]
        return render(request,
                      'document/add_issue.html',
                      {'form': form,
                       'deliver_forms': deliver_forms,

                       'count': count,
                       'count_range': count_range,
                       })


def edit_issue(request, slug):
    """
    Редактирование отчета
    """
    if request.method == 'POST':
        form = AddIssueForm(request.POST)
        models = DetailInfo.objects.filter(issuance_accounting__slug=slug)
        count = models.count()
        deliver_forms = [AddDetailInfoForm(number, request.POST) for number in range(1, count + 1)]
        deliver_forms_is_valid = all(list(map(lambda dev_form: dev_form.is_valid(), deliver_forms)))

        if form.is_valid() and deliver_forms_is_valid:
            issuance_accounting = get_object_or_404(IssuanceAccounting,
                                                    slug=slug)
            issuance_accounting.product_name = form.cleaned_data['product_name']
            issuance_accounting.issue_code = form.cleaned_data['issue_code']
            issuance_accounting.brand_code = form.cleaned_data['brand_code']
            issuance_accounting.organization_name = form.cleaned_data['organization_name']
            issuance_accounting.save(update_fields=['product_name', 'issue_code', 'brand_code', 'organization_name'])

            details = DetailInfo.objects.filter(issuance_accounting=issuance_accounting)

            for index, deliver_form in enumerate(deliver_forms, 1):
                detail = details[index - 1]
                detail.car_numder = deliver_form.cleaned_data[f'car_number_{index}']
                detail.car_model = deliver_form.cleaned_data[f'car_model_{index}']
                detail.waybill_number = deliver_form.cleaned_data[f'waybill_number_{index}']
                detail.deliver_full_name = deliver_form.cleaned_data[f'deliver_full_name_{index}']
                detail.deliver_number = deliver_form.cleaned_data[f'deliver_number_{index}']
                detail.issued_by = deliver_form.cleaned_data[f'issued_by_{index}']
                detail.save()

        return redirect('document_info',
                        document_slug=slug)

    else:
        models = DetailInfo.objects.filter(issuance_accounting__slug=slug)
        count = models.count()
        detail_info_form = [EditDetailInfoForm(model, number) for number, model in
                            zip(list(range(1, count + 1)), models)]
        issuance_accounting = IssuanceAccounting.objects.filter(slug=slug).first()
        form = EditIssueForm(issuance_accounting)
        detail_info = DetailInfo.objects.filter(issuance_accounting_id=issuance_accounting.id)
        cost_accounting_balances = CostAccountingBalances.objects.filter(slug=slug)
        return render(request,
                      'document/edit_issue.html',
                      {'Issuance_Accounting': issuance_accounting,
                       'Detail_Info': detail_info,
                       'form': form,
                       'deliver_forms': detail_info_form,
                       'Cost_Accounting_Balances': cost_accounting_balances, })
