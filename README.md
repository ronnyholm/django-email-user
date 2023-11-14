# Django Email User
Standard Django user model except with email address instead of username.
Removes all traces of the username field from the model and django admin.

# Getting started
Install the dependency with pip
```bash
pip install git+ssh://git@github.com/ronnyholm/django-email-user.git
```
Or with poetry
```bash
poetry add git+ssh://git@github.com/ronnyholm/django-email-user.git
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