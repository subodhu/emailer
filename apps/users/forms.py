from django.contrib.auth.forms import UserChangeForm, UserCreationForm

from .models import User


class SignupForm(UserCreationForm):
    class Meta(UserCreationForm):
        model = User
        fields = ("email", "mobile", "name")


class UserUpdateForm(UserChangeForm):
    class Meta:
        model = User
        fields = ("email", "name", "mobile")
