from django.contrib.auth.forms import UserChangeForm as BaseUserChangeForm
from django.contrib.auth.forms import UserCreationForm as BaseUserCreationForm


class UserChangeForm(BaseUserChangeForm):
    pass


class UserCreationForm(BaseUserCreationForm):
    pass
