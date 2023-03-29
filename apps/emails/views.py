from django.http import HttpResponse
from django.utils import timezone
from PIL import Image

from .models import EmailRecipient


def load_image(request, pk):
    """This view dynimically generates a single pixel image and sends
    to the user when user open's the email. The url is added in the email
    body when sending the email. If the email service providers
    uses the proxy to load the images or users' have disabled the image loading
    then we can't know if the user has opened the email or not.
    """
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
