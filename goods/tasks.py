from celery import shared_task
import time

@shared_task
def send_email_task(user_email, order_id):
    print(f"Отправка письма на {user_email} о заказе №{order_id}")
    time.sleep(5)
    print(f"Письмо пользователю {user_email} отправлено")
    return f"Уведомление о заказе {order_id} отправлено на {user_email}"