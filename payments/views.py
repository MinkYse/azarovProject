from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.csrf import csrf_exempt
from .form import PaymentForm, ChildForm
from .models import Child, Hall, Parent
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

            child.save()
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
            return redirect('/info')
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
        data = list(children.values('id', 'full_name'))
        return JsonResponse(data, safe=False)
    return JsonResponse({'error': 'Invalid request'}, status=400)


def payment_success_view(request):
    # Здесь можно обрабатывать успешный платеж
    return render(request, 'payments/payment_success.html')


@login_required
def info_view(request):
    halls = Hall.objects.all()
    selected_hall = request.GET.get('hall')
    children = Child.objects.filter(hall__id=selected_hall) if selected_hall else None

    return render(request, 'payments/info.html', {
        'halls': halls,
        'children': children,
        'selected_hall': selected_hall
    })


def terms_view(request):
    return render(request, 'payments/terms.html')


def privacy_view(request):
    return render(request, 'payments/privacy.html')


def home_view(request):
    return render(request, 'home.html')
