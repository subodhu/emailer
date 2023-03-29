from django.http import HttpResponse
from django.utils import timezone
from PIL import Image

from .models import EmailRecipient


def load_image(request, pk):
    try:
        recipient = EmailRecipient.objects.get(id=pk)
    except EmailRecipient.DoesNotExist:
        pass
    else:
        recipient.read_date = timezone.now().date()
        recipient.save()
        image = Image.new("RGB", (1, 1))
        response = HttpResponse(content_type="image/png", status=200)
        image.save(response, "PNG")
        return response
