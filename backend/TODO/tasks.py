import os

import httpx
from celery import shared_task
from django.utils.timezone import now

from backend.celery import app

from .models import Task


@shared_task
def check_and_notify_tasks():
    tasks_due = Task.objects.filter(
        due_date__lte=now(), notified=False, is_completed=False
    )
    for task in tasks_due:
        text = f"🔔 Напоминание!\nЗадача: {task.title}\nОписание: {task.description}"

        webhook_url = os.getenv("BOT_WEBHOOK_URL")

        payload = {"telegram_id": task.user.telegram_id, "message": text}

        with httpx.Client() as client:
            response = client.post(webhook_url, json=payload)
            response.raise_for_status()

        app.send_task(
            "notification_worker.celery_worker.send_task_notification",
            args=(task.user.telegram_id, text),
        )
        task.notified = True
        task.save()
