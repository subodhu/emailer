from django.contrib import admin

from .models import Email, EmailRecipient, EmailTemplate

admin.site.register([EmailTemplate, Email, EmailRecipient])
