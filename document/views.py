from django.shortcuts import render, redirect, get_object_or_404, HttpResponse
from django.urls import reverse
from django.views.decorators.http import require_POST

from account.models import CustomUser
from .models import DetailInfo, IssuanceAccounting, DeliverDetail, CostAccountingBalances, Commision
from .forms import AddIssueForm, AddDetailInfoForm, EditDetailInfoForm, EditIssueForm, EditCommisionForm, \
    EditDeliverDetailForm, AddCommisionForm, AddDeliverDetailForm
import datetime
import re

from django.contrib.auth.decorators import login_required


def create_slug(name: str) -> str:
    slug = name.lower().strip()
    slug = re.sub(r'[^\w\s-]', '', slug)
    slug = re.sub(r'[\s_-]+', '-', slug)
    slug = re.sub(r'^-+|-+$', '', slug)
    return slug


# Create your views here.

@login_required
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

@login_required
def issuance_info(request, document_slug=None):
    """
    Представление для отображения информации о учета выдачи
    """
    issuance_accounting = get_object_or_404(IssuanceAccounting,
                                            slug=document_slug)
    detail_info = DetailInfo.objects.filter(
        issuance_accounting_id=issuance_accounting.id)
    cost_accounting_balances = CostAccountingBalances.objects.filter(
        slug=document_slug)
    return render(request,
                  'document/issuance_info.html',
                  {'Issuance_Accounting': issuance_accounting,
                   'Detail_Info': detail_info,
                   'Cost_Accounting_Balances': cost_accounting_balances, })

@login_required
def cost_info(request, cost_slug=None):
    """
    Представление для отображения информации о учета выдачи
    """
    cost_accounting = get_object_or_404(CostAccountingBalances,
                                        slug=cost_slug)
    commission = Commision.objects.filter(cost=cost_accounting)
    delivers = DeliverDetail.objects.filter(cost=cost_accounting)
    return render(request,
                  'document/cost_info.html',
                  {'Cost_Accounting': cost_accounting,
                   'Delivers': delivers,
                   'Commission': commission, })

@login_required
def add_issuance(request):
    """
    Добаление отчета
    """
    count = int(request.GET.get('count', 0))
    count = count + 1
    count_range = range(0, count)
    if request.method == 'POST':
        form = AddIssueForm(request.POST)
        deliver_forms = [AddDetailInfoForm(
            number, request.POST) for number in range(1, count + 2)]
        deliver_forms_is_valid = all(
            list(map(lambda dev_form: dev_form.is_valid(), deliver_forms)))
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
                    deliver_full_name=deliver_form.cleaned_data[
                        f'deliver_full_name_{index}'],
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
        deliver_forms = [AddDetailInfoForm(number)
                         for number in range(1, count + 1)]
        return render(request,
                      'document/add_issue.html',
                      {'form': form,
                       'deliver_forms': deliver_forms,

                       'count': count,
                       'count_range': count_range,
                       })



@login_required
def edit_issue(request, slug):
    """
    Редактирование отчета
    """
    if request.method == 'POST':
        form = AddIssueForm(request.POST)
        models = DetailInfo.objects.filter(issuance_accounting__slug=slug)
        count = models.count()
        deliver_forms = [AddDetailInfoForm(
            number, request.POST) for number in range(1, count + 1)]
        deliver_forms_is_valid = all(
            list(map(lambda dev_form: dev_form.is_valid(), deliver_forms)))

        if form.is_valid() and deliver_forms_is_valid:
            issuance_accounting = get_object_or_404(IssuanceAccounting,
                                                    slug=slug)
            issuance_accounting.product_name = form.cleaned_data['product_name']
            issuance_accounting.issue_code = form.cleaned_data['issue_code']
            issuance_accounting.brand_code = form.cleaned_data['brand_code']
            issuance_accounting.organization_name = form.cleaned_data['organization_name']
            issuance_accounting.save(
                update_fields=['product_name', 'issue_code', 'brand_code', 'organization_name'])

            details = DetailInfo.objects.filter(
                issuance_accounting=issuance_accounting)

            for index, detail_form in enumerate(deliver_forms, 1):
                detail = details[index - 1]
                detail.car_numder = detail_form.cleaned_data[f'car_number_{index}']
                detail.car_model = detail_form.cleaned_data[f'car_model_{index}']
                detail.waybill_number = detail_form.cleaned_data[
                    f'waybill_number_{index}']
                detail.deliver_full_name = detail_form.cleaned_data[
                    f'deliver_full_name_{index}']
                detail.deliver_number = detail_form.cleaned_data[
                    f'deliver_number_{index}']
                detail.issued_by = detail_form.cleaned_data[f'issued_by_{index}']
                detail.save()

        return redirect('document_info',
                        document_slug=slug)

    else:
        models = DetailInfo.objects.filter(issuance_accounting__slug=slug)
        count = models.count()
        detail_info_form = [EditDetailInfoForm(model, number) for number, model in
                            zip(list(range(1, count + 1)), models)]
        issuance_accounting = IssuanceAccounting.objects.filter(
            slug=slug).first()
        form = EditIssueForm(issuance_accounting)
        detail_info = DetailInfo.objects.filter(
            issuance_accounting_id=issuance_accounting.id)
        cost_accounting_balances = CostAccountingBalances.objects.filter(
            slug=slug)
        return render(request,
                      'document/edit_issue.html',
                      {'Issuance_Accounting': issuance_accounting,
                       'Detail_Info': detail_info,
                       'form': form,
                       'deliver_forms': detail_info_form,
                       'Cost_Accounting_Balances': cost_accounting_balances, })

@login_required
def add_cost(request):
    """
    Добаление учета выдачи
    """
    count_commission = int(request.GET.get('count_commission', 1))

    count_delivers = int(request.GET.get('count_delivers', 1))

    if bool(request.GET.get('com', False)):
        count_commission = count_commission + 1
    elif bool(request.GET.get('del', False)):
        count_delivers = count_delivers + 1
    date = datetime.date.today()
    time = datetime.datetime.now().strftime("%H:%M:%S")

    if request.method == 'POST':

        commission_forms = [AddCommisionForm(
            number, request.POST) for number in range(1, count_commission + 1)]
        commission_forms_is_valid = all(
            list(map(lambda com_form: com_form.is_valid(), commission_forms)))

        deliver_detail_forms = [AddDeliverDetailForm(number, request.POST) for number in
                                range(1, count_delivers + 1)]
        deliver_detail_forms_is_valid = all(
            list(map(lambda dev_form: dev_form.is_valid(), deliver_detail_forms)))

        cost_slug = create_slug(str(str(request.user.id) + '-' +
                                    str(date)) + '-' + str(time))

        if deliver_detail_forms_is_valid and commission_forms_is_valid:
            try:
                pk = CostAccountingBalances.objects.create(
                    user=get_object_or_404(CustomUser,
                                           id=request.user.id),
                    date=date,
                    time=time,
                    slug=cost_slug
                ).id

                # pk = CostAccountingBalances.objects.filter(
                #     user=request.user.id,
                #     date=date,
                #     slug=cost_slug
                # ).first().id
            except:
                pass
            for index, commission_form in enumerate(commission_forms, 1):
                Commision.objects.create(
                    full_name=commission_form.cleaned_data[f'com_full_name_{index}'],
                    position=commission_form.cleaned_data[f'position_{index}'],
                    cost=get_object_or_404(CostAccountingBalances,
                                           user=request.user.id,
                                           date=date,
                                           id=pk)
                )
            for index, deliver_form in enumerate(deliver_detail_forms, 1):
                DeliverDetail.objects.create(
                    brand_of_equipment=deliver_form.cleaned_data[
                        f'brand_of_equipment_{index}'],
                    garage_number=deliver_form.cleaned_data[f'garage_number_{index}'],
                    body_number=deliver_form.cleaned_data[
                        f'body_number_{index}'],
                    full_name=deliver_form.cleaned_data[
                        f'full_name_{index}'],
                    speedometer_reading=deliver_form.cleaned_data[
                        f'speedometer_reading_{index}'],
                    fuel_brand=deliver_form.cleaned_data[f'fuel_brand_{index}'],
                    remaining_fuel=deliver_form.cleaned_data[
                        f'remaining_fuel_{index}'],
                    cost=get_object_or_404(CostAccountingBalances,
                                           user=request.user.id,
                                           date=date,
                                           id=pk)
                )

        return redirect('cost_info',
                        cost_slug=cost_slug)
    else:
        # form = AddIssueForm()
        # deliver_form = AddDetailInfo()

        commission_forms = [AddCommisionForm(number)
                            for number in range(1, count_commission + 1)]
        deliver_forms = [AddDeliverDetailForm(number)
                         for number in range(1, count_delivers + 1)]
        return render(request,
                      'document/add_cost.html',
                      {
                          'commission_forms': commission_forms,
                          'deliver_forms': deliver_forms,
                          'date': date,

                          'count_delivers': count_delivers,

                          'count_commission': count_commission,

                      })

@login_required
def edit_cost_accounting(request, slug):
    """Редактирование расходов ГСМ"""
    if request.method == 'POST':
        commission_models = Commision.objects.filter(cost__slug=slug)
        commission_count = commission_models.count()
        commission_forms = [AddCommisionForm(
            number, request.POST) for number in range(1, commission_count + 1)]
        commission_forms_is_valid = all(
            list(map(lambda com_form: com_form.is_valid(), commission_forms)))

        deliver_detail_models = DeliverDetail.objects.filter(cost__slug=slug)
        deliver_detail_count = deliver_detail_models.count()
        deliver_detail_forms = [AddDeliverDetailForm(number, request.POST) for number in
                                range(1, deliver_detail_count + 1)]
        deliver_detail_forms_is_valid = all(
            list(map(lambda dev_form: dev_form.is_valid(), deliver_detail_forms)))
        if deliver_detail_forms_is_valid and commission_forms_is_valid:
            for index, commission_form in enumerate(commission_forms, 1):
                commission = commission_models[index - 1]
                commission.full_name = commission_form.cleaned_data[
                    f'com_full_name_{index}']
                commission.position = commission_form.cleaned_data[f'position_{index}']
                commission.save()

            for index, deliver_form in enumerate(deliver_detail_forms, 1):
                deliver = deliver_detail_models[index - 1]
                deliver.brand_of_equipment = deliver_form.cleaned_data[
                    f'brand_of_equipment_{index}']
                deliver.garage_number = deliver_form.cleaned_data[f'garage_number_{index}']
                deliver.body_number = deliver_form.cleaned_data[
                    f'body_number_{index}']
                deliver.full_name = deliver_form.cleaned_data[
                    f'full_name_{index}']
                deliver.speedometer_reading = deliver_form.cleaned_data[
                    f'speedometer_reading_{index}']
                deliver.fuel_brand = deliver_form.cleaned_data[f'fuel_brand_{index}']
                deliver.remaining_fuel = deliver_form.cleaned_data[
                    f'remaining_fuel_{index}']
                deliver.save()
            return redirect('cost_info',
                            cost_slug=slug)

    else:
        cost_accounting = get_object_or_404(CostAccountingBalances, slug=slug)
        commission_models = Commision.objects.filter(cost__slug=slug)
        commission_count = commission_models.count()
        commission_form = [EditCommisionForm(commission_models, number) for number, commission_models in
                           zip(list(range(1, commission_count + 1)), commission_models)]

        deliver_detail_models = DeliverDetail.objects.filter(cost__slug=slug)
        deliver_detail_count = deliver_detail_models.count()

        deliver_detail_forms = [EditDeliverDetailForm(deliver_detail_models, number)
                                for number, deliver_detail_models in
                                zip(list(range(1, deliver_detail_count + 1)), deliver_detail_models)]

        return render(request,
                      'document/edit_cost.html',
                      {'Cost_Accounting': cost_accounting,
                       'commission_form': commission_form,
                       'deliver_detail_forms': deliver_detail_forms, })

@login_required
def delete_cost_accounting(request, slug):
    """Удаление расходов ГСМ"""
    cost_accounting = get_object_or_404(CostAccountingBalances, slug=slug)
    cost_accounting.delete()
    return redirect('show_documents')

@login_required
def delete_issue(request, slug):
    """Удаление выдачи ГСМ"""
    issue = get_object_or_404(IssuanceAccounting, slug=slug)
    issue.delete()
    return redirect('show_documents')
