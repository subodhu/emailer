from django.urls import path

from .views import load_image

urlpatterns = [path("load-image/<int:pk>/", load_image, name="load_image")]
