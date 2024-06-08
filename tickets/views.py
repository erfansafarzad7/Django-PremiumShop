from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import FormView, ListView
from django.urls import reverse_lazy
from .forms import CreateTicketForm
from .models import Ticket


class TicketView(LoginRequiredMixin, FormView):
    model = Ticket
    form_class = CreateTicketForm
    template_name = 'tickets/send_ticket.html'
    success_url = reverse_lazy('tickets:all')

    def form_valid(self, form):
        form.instance.user = self.request.user
        form.instance.status = 'Sent'
        form.save()
        print('succccc')
        return super().form_valid(form)

    def form_invalid(self, form):
        print(form.errors)
        return super().form_invalid(form)

    def post(self, request, *args, **kwargs):
        print('post')
        return super().post(request, *args, **kwargs)

    def get(self, request, *args, **kwargs):
        print('geet')
        return super().get(request, *args, **kwargs)


class MyTicketView(LoginRequiredMixin, ListView):
    model = Ticket
    template_name = 'tickets/my_tickets.html'
    context_object_name = 'my_tickets'

    def get_queryset(self):
        return Ticket.objects.filter(user_id=self.request.user.id).order_by('-created_date')
