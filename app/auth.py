from django.contrib.auth.backends import ModelBackend
from django.db.models import Q

from app.models import MyUser


class MyBackend(ModelBackend):
    def authenticate(self, request, username=None, password=None, **kwargs):
        user = MyUser.objects.filter(Q(phone=username)|Q(username=username)).first()
        if user:
            if user.check_password(password):
                return user
            else:
                return None
        else:
            return None
