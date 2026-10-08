import time
from celery import shared_task
from django.core.mail import send_mail
from django.conf import settings
from django.contrib.sessions.models import Session
from django.utils import timezone

@shared_task
def generate_books_catalog_pdf_task(user_email: str):
    print(f"Начало генерации каталога для {user_email}...")
    time.sleep(5)
    print(f"Каталог успешно сгенерирован и отправлен на {user_email}!")
    return f"Catalog sent to {user_email}"

@shared_task
def clear_expired_sessions_task():
    now = timezone.now()
    expired_sessions = Session.objects.filter(expire_date__lt=now)
    count = expired_sessions.count()
    expired_sessions.delete()
    print(f"Периодическая очистка: удалено просроченных сессий: {count}")
    return f"Cleared {count} sessions"

@shared_task
def send_book_return_reminder_task(user_email: str, book_title: str):
    subject = "Напоминание о возврате книги"
    message = f"Здравствуйте!\n\nНапоминаем, что срок аренды книги '{book_title}' подходит к концу. Пожалуйста, верните её."
    
    try:
        send_mail(
            subject=subject,
            message=message,
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[user_email],
            fail_silently=False,
        )
        print(f"Email успешно отправлен на {user_email}")
        return f"Email sent to {user_email}"
    except Exception as e:
        print(f"Ошибка при отправке email: {str(e)}")
        return f"Failed: {str(e)}"
