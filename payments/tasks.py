# your_app/tasks.py
from celery import shared_task
import telegram

import asyncio
from .models import Child, Application

from .parser import fetch_emails_from_yandex


@shared_task
def reset_is_paid():
    token = '7532743180:AAEqoxGi2PMFEoVEDNeWw3-qCu181mVcX4M'
    bot = telegram.Bot(token=token)
    user_id = '849192412'
    unpaid_children = Child.objects.filter(is_paid=False, active=True, is_vip=False)

    # Если есть такие дети, формируем сообщение
    if unpaid_children.exists():
        message = "Дети, которые не оплатили:\n\n"
        for child in unpaid_children:
            message += f"👦 Ученик: {child.full_name}\n"
            message += f"🏠 Зал: {child.hall.name}\n"
            message += f"📚 Опция тренировки: {child.training_option.name}\n"
            message += "👨‍👩‍👧‍👦 Родители:\n"
            for parent in child.parents.all():
                phone_link = f"tel:{parent.phone_number}"  # Формируем ссылку для звонка
                message += f'    📛 Имя: {parent.full_name}\n'
                message += f'    ☎️ Телефон: <a href="{phone_link}">{parent.phone_number}</a>\n'
            message += "\n"  # Добавляем отступ между детьми
    else:
        message = "Все дети оплатили."

    asyncio.run(bot.send_message(chat_id=user_id, text=message, parse_mode='HTML'))
    Child.objects.filter(is_vip=False, active=True).update(is_paid=False)


@shared_task
def pars_email():
    fetch_emails_from_yandex()
