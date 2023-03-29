from django.db import models
from django.utils.translation import gettext_lazy as _

from apps.core.models import TimestampAbstractModel
from apps.users.models import User


class EmailTemplate(TimestampAbstractModel):
    name = models.CharField(_("template name"), max_length=56)
    template = models.TextField()
    created_by = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="email_templates",
    )
    updated_by = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        blank=True,
        null=True,
    )

    class Meta:
        verbose_name = _("email template")
        verbose_name_plural = _("email templates")

    def __str__(self):
        return self.name


class Email(TimestampAbstractModel):
    user = models.ForeignKey(User, related_name="emails", on_delete=models.CASCADE)
    template = models.ForeignKey(
        EmailTemplate, related_name="emails", on_delete=models.CASCADE
    )
    subject = models.CharField(_("subject"), max_length=128)
    body = models.TextField(_("body"))
    created_by = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="created_emails",
    )
    # if send time is null then email is sent at soon as it is created
    send_time = models.DateTimeField(blank=True, null=True)
    updated_by = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="updated_emails",
        blank=True,
        null=True,
    )

    class Meta:
        verbose_name = _("email")
        verbose_name_plural = _("emails")

    def __str__(self):
        return self.body


class EmailRecipient(TimestampAbstractModel):
    email = models.ForeignKey(
        Email, related_name="email_recipients", on_delete=models.CASCADE
    )
    recipient_email = models.EmailField(_("recipient email"))
    sent_date = models.DateTimeField(_("email sent date"), blank=True, null=True)
    read_date = models.DateTimeField(_("email read date"), blank=True, null=True)
    failed_count = models.IntegerField(default=0)
    created_by = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="email_recipients",
    )
    updated_by = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        blank=True,
        null=True,
    )

    class Meta:
        verbose_name = _("email recipient")
        verbose_name_plural = _("emails recipients")

    def __str__(self):
        return self.recipient_email
