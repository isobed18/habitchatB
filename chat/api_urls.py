from django.urls import path
from chat.views import chat_room

urlpatterns = [
    path("chat/", chat_room, name="chat_room"),
]
