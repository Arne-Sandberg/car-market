from __future__ import absolute_import, unicode_literals
from celery import shared_task
from django.core.mail import EmailMessage


@shared_task
def send_message(reciever, subject, msg):
    EmailMessage(
        subject=subject,
        body=msg,
        to=[reciever],
    ).send()
