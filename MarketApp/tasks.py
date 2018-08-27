from __future__ import absolute_import, unicode_literals
from celery import shared_task
from django.core import mail
from django.core.mail import EmailMessage


@shared_task
def send_message(reciever, subject, msg):
        EmailMessage(
            subject=subject,
            body=msg,
            to=[reciever],
        ).send()
        res = mail.outbox.pop()
        print(res.body, res.to)

