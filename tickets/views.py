from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import FormView, ListView, RedirectView
from django.urls import reverse_lazy
from django.contrib.messages.views import SuccessMessageMixin
from .forms import CreateTicketForm
from .models import Ticket


class TicketView(LoginRequiredMixin, SuccessMessageMixin, FormView, RedirectView):
    model = Ticket
    form_class = CreateTicketForm
    template_name = 'tickets/send_ticket.html'
    success_url = reverse_lazy('tickets:all')
    success_message = 'تیکت شما با موفقیت ارسال شد..'

    def get_redirect_url(self, *args, **kwargs):
        return reverse_lazy('tickets:all')

    def form_valid(self, form):
        form.instance.user = self.request.user
        form.instance.status = 'ارسال شد'
        form.save()
        return super().form_valid(form)


class MyTicketView(LoginRequiredMixin, ListView):
    model = Ticket
    template_name = 'tickets/my_tickets.html'
    context_object_name = 'my_tickets'

    def get_queryset(self):
        return Ticket.objects.filter(user_id=self.request.user.id).order_by('-created_date')
