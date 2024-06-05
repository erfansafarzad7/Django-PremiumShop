from django.shortcuts import render
from django.views.generic import FormView
from django.urls import reverse_lazy
from .forms import CreateTicketForm
from .models import Ticket


class TicketView(FormView):
    form_class = CreateTicketForm
    template_name = 'tickets/all_tickets.html'
    success_url = reverse_lazy('tickets:all')

    def form_valid(self, form):
        cd = form.cleaned_data
        form.instance.user = self.request.user
        form.instance.status = 'Sent'
        form.save()
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context['all_tickets'] = Ticket.objects.filter(user__exact=self.request.user)

        return context
