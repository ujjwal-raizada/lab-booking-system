from time import sleep
from django.conf import settings
from django.core.mail import send_mass_mail
from django.core.management.base import BaseCommand

from ...models.email import EmailModel

MAX_EMAIL_PER_COMMAND = 30
SLEEP_PER_LOOP = 60

class Command(BaseCommand):
    help = 'Always running management command to send all queued emails'

    def handle(self, *args, **options):
        while True:
            emails = EmailModel.objects.filter(sent=False).order_by('date_time')[:MAX_EMAIL_PER_COMMAND]
            datatuple = []
            for email in emails:
                message = (
                    email.subject,
                    email.text,
                    settings.EMAIL_HOST_USER,
                    [email.receiver],
                )
                datatuple.append(message)
                email.sent = True
            send_mass_mail(datatuple, fail_silently=False)

            EmailModel.objects.bulk_update(emails, ['sent'])
            sleep(SLEEP_PER_LOOP)


