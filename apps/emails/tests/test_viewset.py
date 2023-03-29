from django.test import TestCase
from rest_framework.test import APIRequestFactory, force_authenticate

from apps.emails.api.v1.views import EmailTemplateViewSet, EmailViewSet
from apps.emails.models import Email, EmailRecipient, EmailTemplate
from apps.users.models import User

EMAIL_TEMPLATE = """
<!DOCTYPE html>
<html lang="en">
  <head>
    <meta charset="UTF-8" />
    <title>{{ subject }}</title>
  </head>
  <body>
    <h5>Hello {{ to_email }},</h5>

    <p>{{ body }}</p> <br>
    <p>Regards</p>
    {{ sender_name }}
    <img src="{{ image_url }}" />
  </body>
</html>
"""


class EmailTemplateViewSetTest(TestCase):
    def setUp(self):
        self.factory = APIRequestFactory()
        self.admin = User.objects.create_superuser(
            password="adminemailer", email="admin@emailer.com"
        )
        self.user = User.objects.create_user(
            password="helloemailer", email="user@emailer.com"
        )

    def test_template_get(self):
        request = self.factory.get("/api/v1/email-templates/")
        EmailTemplate.objects.create(
            name="template", template=EMAIL_TEMPLATE, created_by=self.admin
        )
        force_authenticate(request, user=self.user)
        response = EmailTemplateViewSet.as_view({"get": "list"})(request)
        self.assertEqual(response.data["results"][0]["name"], "template")
        self.assertEqual(response.status_code, 200)

    def test_template_post(self):
        data = {"name": "template 1", "template": EMAIL_TEMPLATE}
        request = self.factory.post("/api/v1/email-templates/", data, format="json")
        force_authenticate(request, user=self.admin)
        response = EmailTemplateViewSet.as_view({"post": "create"})(request)
        self.assertEqual(response.data["name"], "template 1")
        self.assertEqual(response.status_code, 201)

    def test_template_delete(self):
        template = EmailTemplate.objects.create(
            name="template", template=EMAIL_TEMPLATE, created_by=self.admin
        )
        request = self.factory.delete("/api/v1/email-templates/")
        force_authenticate(request, user=self.admin)
        response = EmailTemplateViewSet.as_view({"delete": "destroy"})(
            request, pk=template.id
        )
        self.assertEqual(response.status_code, 204)


class EmailViewSetTest(TestCase):
    def setUp(self):
        self.factory = APIRequestFactory()
        self.admin = User.objects.create_superuser(
            password="adminemailer", email="admin@emailer.com"
        )
        self.user = User.objects.create_user(
            password="helloemailer", email="user@emailer.com"
        )

    def test_email_get(self):
        request = self.factory.get("/api/v1/emails/")
        template = EmailTemplate.objects.create(
            name="template", template=EMAIL_TEMPLATE, created_by=self.admin
        )
        email = Email.objects.create(
            user=self.user,
            template=template,
            subject="Hello",
            body="Hello World",
            created_by=self.user,
        )
        EmailRecipient.objects.create(
            email=email, recipient_email="reciver@test.com", created_by=self.user
        )
        force_authenticate(request, user=self.user)
        response = EmailViewSet.as_view({"get": "list"})(request)
        self.assertEqual(response.data["results"][0]["subject"], "Hello")
        self.assertEqual(response.status_code, 200)

    def test_template_post(self):
        template = EmailTemplate.objects.create(
            name="template", template=EMAIL_TEMPLATE, created_by=self.admin
        )
        data = {
            "template": template.id,
            "subject": "Hello",
            "body": "World",
            "recipients": [{"recipient_email": "user@example.com"}],
        }
        request = self.factory.post("/api/v1/emails/", data, format="json")
        force_authenticate(request, user=self.admin)
        response = EmailViewSet.as_view({"post": "create"})(request)
        self.assertEqual(response.data["subject"], "Hello")
        self.assertEqual(response.status_code, 201)
