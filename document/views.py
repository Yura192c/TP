from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.http import require_POST

from account.models import CustomUser
from .models import DetailInfo, IssuanceAccounting, DeliverDetail, CostAccountingBalances
from .forms import AddIssue, AddIssue_no_model, AddDetailInfo
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
    if not request.user.is_authenticated:
        pass
        # return redirect('account:login')
    user = request.user.id
    Issuance_Accounting = IssuanceAccounting.objects.filter(user=user)
    Cost_Accounting_Balances = CostAccountingBalances.objects.filter(user=user)
    return render(request,
                  'account/dashboard.html',
                  {'Issuance_Accounting': Issuance_Accounting,
                   'Cost_Accounting_Balances': Cost_Accounting_Balances, })
    # return render(request, 'document/document.html')


def issuance_info(request, document_slug=None):
    issuance_accounting = get_object_or_404(IssuanceAccounting,
                                            slug=document_slug)
    Detail_Info = DetailInfo.objects.filter(issuance_accounting_id=issuance_accounting.id)
    Cost_Accounting_Balances = CostAccountingBalances.objects.filter(slug=document_slug)
    return render(request,
                  'document/issuance_info.html',
                  {'Issuance_Accounting': issuance_accounting,
                   'Detail_Info': Detail_Info,
                   'Cost_Accounting_Balances': Cost_Accounting_Balances, })


def cost_info(request, cost_slug=None):
    cost_accounting = get_object_or_404(CostAccountingBalances,
                                        slug=cost_slug)
    delivers = DeliverDetail.objects.filter(cost=cost_accounting)
    # Detail_Info = DetailInfo.objects.filter(issuance_accounting_id=issuance_accounting.id)
    # Cost_Accounting_Balances = CostAccountingBalances.objects.filter(slug=document_slug)
    return render(request,
                  'document/cost_info.html',
                  {
                      'Cost_Accounting': cost_accounting,
                      'Delivers': delivers,
                  })


# def add_deliver(request, count):
#     request.GET

# @require_POST
def add_issance(request):
    '''
    Добаление отчета
    '''
    count = int(request.GET.get('count', 0))
    # if count == 0:
    count = count + 1
    count_range = range(0, count)
    # req = request.POST
    if request.method == 'POST':
        form = AddIssue_no_model(request.POST)
        deliver_forms = [AddDetailInfo(number, request.POST) for number in range(1, count + 2)]
        deliver_forms_is_valid = all(list(map(lambda dev_form: dev_form.is_valid(), deliver_forms)))
        if form.is_valid() and deliver_forms_is_valid:
            try:

                IssuanceAccounting.objects.create(
                    # user=request.user.id,
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
        form = AddIssue_no_model()
        # deliver_form = AddDetailInfo()
        deliver_forms = [AddDetailInfo(number) for number in range(1, count + 1)]
        return render(request,
                      'document/add_issue.html',
                      {'form': form,
                       'deliver_forms': deliver_forms,

                       'count': count,
                       'count_range': count_range,
                       })


def modal_add(request):
    pass
