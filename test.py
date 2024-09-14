import imaplib
import email
from email.header import decode_header
import re


def fetch_emails_from_yandex():
    # Ваши учетные данные
    username = "azarov-taekwondo@yandex.ru"
    password = "ogxecuvafpwzhzss"

    # Подключение к почтовому серверу Яндекса через IMAP
    imap = imaplib.IMAP4_SSL("imap.yandex.com")

    # Логинимся
    imap.login(username, password)

    # Выбираем папку "INBOX"
    imap.select("inbox")

    # Ищем все непрочитанные письма с домена @wixforms.com
    status, messages = imap.search(None, '(UNSEEN FROM "@wixforms.com")')

    email_ids = messages[0].split()

    # Печатаем общее количество найденных писем
    print(f"Found {len(email_ids)} new emails.")

    for email_id in email_ids:
        status, msg_data = imap.fetch(email_id, "(RFC822)")
        for response_part in msg_data:
            if isinstance(response_part, tuple):
                msg = email.message_from_bytes(response_part[1])
                subject, encoding = decode_header(msg["Subject"])[0]
                if isinstance(subject, bytes):
                    subject = subject.decode(encoding)
                sender = msg.get("From")
                print(f"Subject: {subject}, From: {sender}")

                # Проверяем, является ли сообщение мультичастным
                if msg.is_multipart():
                    for part in msg.walk():
                        if part.get_content_type() == "message/rfc822":
                            # Это пересланное сообщение, его нужно разобрать отдельно
                            forwarded_msg = email.message_from_bytes(part.get_payload(decode=True))
                            process_forwarded_message(forwarded_msg)
                        elif part.get_content_type() == "text/plain":
                            body = part.get_payload(decode=True).decode()
                            print(f"Body: {body}")
                else:
                    body = msg.get_payload(decode=True).decode()
                    print(f"Body: {body}")

    # Закрываем соединение с сервером
    imap.close()
    imap.logout()


def process_forwarded_message(forwarded_msg):
    """
    Функция для обработки пересланных сообщений.
    """
    subject, encoding = decode_header(forwarded_msg["Subject"])[0]
    if isinstance(subject, bytes):
        subject = subject.decode(encoding)
    sender = forwarded_msg.get("From")
    print(f"Forwarded Subject: {subject}, From: {sender}")

    if forwarded_msg.is_multipart():
        for part in forwarded_msg.walk():
            if part.get_content_type() == "text/plain":
                body = part.get_payload(decode=True).decode()
                print(f"Forwarded Body: {body}")
    else:
        body = forwarded_msg.get_payload(decode=True).decode()
        print(f"Forwarded Body: {body}")


fetch_emails_from_yandex()
body = """Подробности:
Имя: Виктор
Эл. почта: skaz07@list.ru
Телефон: +79107222808
Сообщение: Виктор 8 лет"""

data = {}

name_match = re.search(r"Имя: (.+)", body)
email_match = re.search(r"Эл. почта: (.+)", body)
phone_match = re.search(r"Телефон: (.+)", body)
message_match = re.search(r"Сообщение: (.+)", body)

# Извлекаем данные, если найдено
data['name'] = name_match.group(1).strip() if name_match else None
data['email'] = email_match.group(1).strip() if email_match else None
data['phone'] = phone_match.group(1).strip() if phone_match else None
data['message'] = message_match.group(1).strip() if message_match else None

print(data)
