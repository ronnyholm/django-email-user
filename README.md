# Django 4.2 Email User
Standard Django user model except with email address instead of username.
Removes all traces of the username field from the model and django admin.

# Getting started
Install the dependency with pip
```bash
pip install git+https://github.com/ronnyholm/django-email-user.git
```
Or with poetry
```bash
poetry add git+https://github.com/ronnyholm/django-email-user.git
```

Update `AUTH_USER_MODEL` in `settings.py`
```python
# settings.py
AUTH_USER_MODEL = "email_user.User"
```

# Usage
Always use `django.contrib.auth.get_user_model()` when referencing the user model.

```python
from django.contrib.auth import get_user_model()
User = get_user_model()

# Create a new user
user = User(email="john.doe@example.com", first_name="John", last_name="Doe")
user.save()

# Querying
all_the_johns = User.objects.filter(first_name="John")
```

## Fixing django admin grouping
By default Django will separate the `Group` and the new `User` models since they come from two separate apps, to fix this we can create proxies for them under a new app. I've found this to be the least hacky method.
```bash
python manage.py startapp users
```

Edit the `users/app.py` file to give it a decent verbose name
```python
# users/app.py
from django.apps import AppConfig


class UsersConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "users"
    verbose_name = "Authentication and Authorization"
```

Proxy the old group and new user models into this app
```python
# users/models.py
from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group
User = get_user_model()

class UserProxy(User):
    class Meta:
        proxy = True
        verbose_name = "user"
        verbose_name_plural = "users"

class GroupProxy(Group):
    class Meta:
        proxy = True
        verbose_name = "group"
        verbose_name_plural = "groups"
```

Unregister the old models and register the new proxies
```python
# users/admin.py
from django.contrib import admin
from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group as OldGroup
from django.contrib.auth.admin import GroupAdmin
from email_user.admin import UserAdmin
from .models import UserProxy, GroupProxy
OldUser = get_user_model()

admin.site.unregister(OldUser)
admin.site.unregister(OldGroup)

admin.site.register(UserProxy, UserAdmin)
admin.site.register(GroupProxy, GroupAdmin)
```

Add the new app to `INSTALLED_APPS`
```python
# your_project/settings.py
...
INSTALLED_APPS = [
  ...
  "your_project",
  "users",
  ...
]
...
```

All done, enjoy your tidy Django admin without the jank and quirks!
