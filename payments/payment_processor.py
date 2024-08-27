from yookassa import Payment
from yookassa.domain.models import Currency


def create_payment(amount, description, child_id):
    payment = Payment.create({
        "amount": {
            "value": str(amount),
            "currency": Currency.RUB
        },
        "confirmation": {
            "type": "redirect",
            "return_url": "http://localhost:8000/payment/success"
        },
        "capture": True,
        "description": description,
        "metadata": {
            "child_id": child_id  # Передаем ID ребенка в метаданных
        }
    })
    return payment
