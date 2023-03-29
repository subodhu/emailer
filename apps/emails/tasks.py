import logging
from smtplib import SMTPException

from django.conf import settings
from django.contrib.sites.models import Site
from django.core.mail import EmailMessage, get_connection
from django.db.models import Q
from django.template import Context, Template
from django.utils import timezone

from config import celery_app

from .models import Email, EmailRecipient

logger = logging.getLogger(__name__)


@celery_app.task(bind=True, max_retries=3)
def task_send_emails(self, email_id):
    try:
        email = Email.objects.get(id=email_id)
    except Email.DoesNotExist:
        logger.info("Email with id %d does not exists." % email_id)
    else:
        recipients = email.email_recipients.filter(
            Q(sent_date__isnull=True) | Q(failed_count=1)
        )
        now = timezone.now()
        today = now.today()
        email_sent_list = []
        failed_list = []
        template = Template(email.template.template)
        domain = Site.objects.get_current().domain

        with get_connection() as connection:
            context = {
                "from_email": settings.DEFAULT_FROM_EMAIL,
                "date": today,
                "sender_name": email.user.name,
                "subject": email.subject,
                "body": email.body,
            }
            for recipient in recipients:
                # we can pass other personal info in the context
                context.update(
                    {
                        "to_email": settings.DEFAULT_FROM_EMAIL,
                        "image_url": f"https://{domain}/emails/load-image/{recipient.id}/",
                    }
                )
                # rendering email for each recipient with respective data
                body = template.render(Context(context))
                msg = EmailMessage(
                    subject=email.subject,
                    body=body,
                    from_email=settings.DEFAULT_FROM_EMAIL,
                    to=[recipient.recipient_email],
                    connection=connection,
                )
                msg.content_subtype = "html"
                try:
                    sent = msg.send()
                except SMTPException:
                    recipient.failed_count += 1
                    failed_list.append(recipient.failed_count)
                else:
                    # sent is 1 on success else 0
                    if sent:
                        recipient.sent_date = today
                        email_sent_list.append(recipient)
                    else:
                        recipient.failed_count += 1
                        failed_list.append(recipient.failed_count)

        EmailRecipient.objects.bulk_update(email_sent_list, ["sent_date", "updated_at"])
        logger.info("Email sent to %d emails." % len(email_sent_list))

        if failed_list:
            EmailRecipient.objects.bulk_update(
                failed_list, ["failed_count", "updated_at"]
            )
            if len(email_sent_list) < len(recipients):
                self.retry(max_retries=1)
