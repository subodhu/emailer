from rest_framework.routers import DefaultRouter

from .views import EmailTemplateViewSet, EmailViewSet

app_name = "emails"


router = DefaultRouter()
router.register(r"emails", EmailViewSet, basename="emails")
router.register(r"email-templates", EmailTemplateViewSet, basename="email_templates")


urlpatterns = router.urls
