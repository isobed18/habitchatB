from django.shortcuts import render

# Create your views here.
from django.shortcuts import render

def chat_room(request):
    return render(request, "chat.html")
