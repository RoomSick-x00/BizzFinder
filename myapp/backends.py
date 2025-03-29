from django.contrib.auth.backends import ModelBackend
from django.contrib.auth import get_user_model
from django.db.models import Q  # ✅ Import Q for queries

CustomUser = get_user_model()

class CustomAuthBackend(ModelBackend):
    def authenticate(self, request, username=None, password=None, **kwargs):
        """
        Allow login with username, email, or phone number.
        """
        user = None
        if username:
            try:
                user = CustomUser.objects.get(
                    Q(username=username) |  # ✅ Correct usage of Q
                    Q(email=username) | 
                    Q(phone_number=username)
                )
            except CustomUser.DoesNotExist:
                return None

        if user and user.check_password(password):
            return user
        return None
