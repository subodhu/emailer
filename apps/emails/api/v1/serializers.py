from django.utils import timezone
from rest_framework import serializers

from apps.emails.models import Email, EmailRecipient, EmailTemplate


class EmailTemplateSerializer(serializers.ModelSerializer):
    class Meta:
        model = EmailTemplate
        fields = ["id", "name", "template"]


class EmailRecipientSerializer(serializers.ModelSerializer):
    class Meta:
        model = EmailRecipient
        fields = ["id", "recipient_email"]


class EmailSerializer(serializers.ModelSerializer):
    recipients = EmailRecipientSerializer(many=True, source="email_recipients")

    class Meta:
        model = Email
        fields = ["id", "template", "subject", "body", "recipients"]

    def create(self, validated_data):
        recipients = validated_data.pop("email_recipients")
        request = self.context["request"]
        email = Email(**validated_data, user=request.user, created_by=request.user)
        email.save()
        recipient_list = []
        now = timezone.now()
        for recipient in recipients:
            recipient_list.append(
                EmailRecipient(
                    email=email,
                    recipient_email=recipient["recipient_email"],
                    created_by=request.user,
                    created_at=now,
                )
            )
        recipients = EmailRecipient.objects.bulk_create(recipient_list)
        email.recipients = recipients
        return email
