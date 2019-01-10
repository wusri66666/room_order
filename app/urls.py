from django.conf.urls import url
from app.views import *


urlpatterns = [
    url(r"register/$",RegisterView.as_view()),
    url(r"login/$",LoginAPI.as_view()),
    url(r"active/(.*)",active),
    url(r"room/$",room),
    url(r"quit/$",quit),
]