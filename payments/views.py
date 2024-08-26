from django.http import JsonResponse
from django.shortcuts import render, redirect
from .form import PaymentForm, ChildForm
from .models import Child, Hall
# from .payment_processor import create_payment


def add_child_view(request):
    if request.method == 'POST':
        form = ChildForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('/info')  # Перенаправляем на страницу списка детей или на другую страницу
    else:
        form = ChildForm()

    return render(request, 'payments/add_child.html', {'form': form})


def payment_view(request):
    if request.method == 'POST':
        form = PaymentForm(request.POST)
        if form.is_valid():
            child = form.cleaned_data['child']
            option = form.cleaned_data['training_option']
            # payment = create_payment(option.price, f"Оплата за обучение {child.full_name}")
            child.is_paid = False  # Платеж еще не завершен
            child.save()
            return redirect('/info')
    else:
        form = PaymentForm()

    return render(request, 'payments/payment_form.html', {'form': form})


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
