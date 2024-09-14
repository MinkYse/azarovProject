from django.contrib.auth.decorators import login_required, user_passes_test
from django.http import JsonResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.csrf import csrf_exempt
from .form import PaymentForm, ChildForm, ApplicationForm
from .models import Child, Hall, Parent, PDFDocument, Trainer, Application
# from .payment_processor import create_payment

import json


@login_required
def add_child_view(request):
    if request.method == 'POST':
        form = ChildForm(request.POST)
        if form.is_valid():
            child = form.save(commit=False)
            child.save()
            # Создание и добавление первого родителя
            parent1 = Parent(
                full_name=form.cleaned_data['parent1'],
                phone_number=form.cleaned_data['parent1_phone_number']
            )
            parent1.save()
            child.parents.add(parent1)

            # Проверка и добавление второго родителя, если данные введены
            if form.cleaned_data['parent2'] and form.cleaned_data['parent2_phone_number']:
                parent2 = Parent(
                    full_name=form.cleaned_data['parent2'],
                    phone_number=form.cleaned_data['parent2_phone_number']
                )
                parent2.save()
                child.parents.add(parent2)
            return redirect('/info')  # Перенаправляем на страницу списка детей или на другую страницу
    else:
        form = ChildForm()
        print(form)

    return render(request, 'payments/add_child.html', {'form': form})


def child_detail_view(request, pk):
    child = get_object_or_404(Child, pk=pk)
    return render(request, 'payments/child_detail.html', {'child': child})


def payment_view(request):
    if request.method == 'POST':
        form = PaymentForm(request.POST)
        if form.is_valid():
            child = form.cleaned_data['child']
            option = form.cleaned_data['training_option']
            # payment = create_payment(option.price, f"Оплата за обучение {child.full_name}", child.id)
            # return redirect(payment.confirmation.confirmation_url)
            return redirect('/home')
    else:
        form = PaymentForm()

    return render(request, 'payments/payment_form.html', {'form': form})


@csrf_exempt
def payment_webhook_view(request):
    if request.method == 'POST':
        try:
            # Получаем данные из POST-запроса и преобразуем их в словарь
            data = json.loads(request.body.decode('utf-8'))

            # Обрабатываем уведомление от YooKassa
            notification = WebhookNotification(data)
            if notification.event == WebhookNotificationEventType.PAYMENT_SUCCEEDED:
                payment_object = notification.object

                # Извлекаем ID платежа и находим соответствующую запись в базе данных
                child_id = payment_object.metadata.get('child_id')
                if child_id:
                    try:
                        child = Child.objects.get(id=child_id)
                        child.is_paid = True
                        child.save()
                        return JsonResponse({'status': 'success'}, status=200)
                    except Child.DoesNotExist:
                        return JsonResponse({'status': 'error', 'message': 'Child not found'}, status=404)

            return JsonResponse({'status': 'unhandled_event'}, status=400)

        except Exception as e:
            return JsonResponse({'status': 'error', 'message': str(e)}, status=400)
    else:
        return JsonResponse({'status': 'invalid_method'}, status=405)


def get_children(request):
    hall_id = request.GET.get('hall_id')
    training_option_id = request.GET.get('training_option_id')
    if hall_id and training_option_id:
        children = Child.objects.filter(hall_id=hall_id, training_option_id=training_option_id)
        data = list(children.values('id', 'full_name', 'training_option__price'))
        return JsonResponse(data, safe=False)
    return JsonResponse({'error': 'Invalid request'}, status=400)


def payment_success_view(request):
    # Здесь можно обрабатывать успешный платеж
    return render(request, 'payments/payment_success.html')


@login_required
def info_view(request):
    halls = Hall.objects.all()
    selected_hall = request.GET.get('hall')
    children = Child.objects.filter(hall__id=selected_hall, active=True) if selected_hall else None

    return render(request, 'payments/info.html', {
        'halls': halls,
        'children': children,
        'selected_hall': selected_hall
    })


def business_summary(request):
    halls = Hall.objects.all()
    trainers = Trainer.objects.all()

    total_income = sum(hall.get_income() for hall in halls)
    total_rent = sum(hall.month_price + hall.additional_expenses for hall in halls)
    total_salary = sum(trainer.calculate_salary() for trainer in trainers)
    total_expenses = total_rent + total_salary
    final_income = total_income - total_expenses  # Чистый доход с учетом всех затрат

    context = {
        'halls': halls,
        'trainers': trainers,
        'total_income': total_income,
        'total_salary': total_salary,
        'total_rent': total_rent,
        'total_expenses': total_expenses,
        'final_income': final_income,
    }

    return render(request, 'business_summary.html', context)


def terms_view(request):
    return render(request, 'payments/terms.html')


def privacy_view(request):
    return render(request, 'payments/privacy.html')


def home_view(request):
    return render(request, 'home.html')


def pdf_page_view(request):
    selected_pdf_id = request.GET.get('pdf')  # Получаем ID выбранного документа из GET-параметров
    selected_pdf = None

    if selected_pdf_id:
        selected_pdf = get_object_or_404(PDFDocument, id=selected_pdf_id)

    pdfs = PDFDocument.objects.all()
    return render(request, 'pdf_page.html', {
        'pdfs': pdfs,
        'selected_pdf': selected_pdf,
        'selected_pdf_id': selected_pdf_id,
    })


def application_list(request):
    applications = Application.objects.all()
    return render(request, 'applications/application_list.html', {'applications': applications})


def application_update(request, pk):
    application = get_object_or_404(Application, pk=pk)
    if request.method == 'POST':
        form = ApplicationForm(request.POST, instance=application)
        if form.is_valid():
            form.save()
            return redirect('/applications')
    else:
        form = ApplicationForm(instance=application)
    return render(request, 'applications/application_update.html', {'form': form, 'application': application})


def admin_check(user):
    return user.is_superuser


@user_passes_test(admin_check)
def admin_page(request):
    pending_applications_count = Application.objects.filter(status=False).count()
    # Здесь вы можете добавить логику для страницы администратора
    return render(request, 'admin-page.html',
                  {'pending_applications_count': pending_applications_count})