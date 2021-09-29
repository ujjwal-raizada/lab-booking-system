from django.conf import settings
from django.core.management.base import BaseCommand

from ...mail import send_mass_html_mail
from ...models.email import EmailModel

MAX_EMAIL_PER_COMMAND = 30


class Command(BaseCommand):
    help = 'Send all queued emails'

    def handle(self, *args, **options):
        emails = EmailModel.objects.filter(sent=False).order_by('date_time')[:MAX_EMAIL_PER_COMMAND]
        datatuple = []
        for email in emails:
            message = (
                email.subject,
                email.text,
                email.text_html,
                settings.EMAIL_HOST_USER,
                [email.receiver],
            )
            datatuple.append(message)
            email.sent = True
        send_mass_html_mail(datatuple, fail_silently=False)

        EmailModel.objects.bulk_update(emails, ['sent'])


