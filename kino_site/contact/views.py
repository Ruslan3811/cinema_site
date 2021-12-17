from django.shortcuts import render
from .models import Contact
from .forms import ContactForm
from django.views.generic import CreateView
from .service import send
import asyncio
from asgiref.sync import async_to_sync, sync_to_async

# Create your views here.

class ContactView(CreateView):
    model = Contact
    form_class = ContactForm
    success_url = "/"

    def form_valid(self, form):
        form.save()
        send(form.instance.email)
        return super().form_valid(form)