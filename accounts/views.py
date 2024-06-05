from django.contrib.auth.views import LoginView
from django.contrib.auth import authenticate, login
from django.urls import reverse_lazy
from django.shortcuts import redirect
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib import messages
from django.views.generic import FormView, CreateView, UpdateView, DetailView
from django.contrib.auth.mixins import LoginRequiredMixin
from .forms import UserCreationForm, ProfileForm, OTPForm
from .models import User, OTP
from orders.models import Order, Cart

from datetime import datetime, timedelta
import random


def generate_otp(user):
    code = random.randint(10000, 99999)
    OTP.objects.create(user=user, code=code)
    return code


def send_otp(user, field):
    code = generate_otp(user)

    match field:
        case 'email':
            print('send ', code, 'to email ', field)

        case 'phone_number':
            print('send ', code, 'to phone ', field)


def update_user(request, session, user_entered_code):
    user = User.objects.get(username__exact=session['username'], email__exact=session['email'])
    otp = OTP.objects.get(user__exact=user, code__exact=user_entered_code)

    if str(user_entered_code) == otp.code:

        if session['register'] in session:
            user.is_verified = True
            user = authenticate(request, username=session['email'], password=session['password'])
            if user:
                login(request, user)
        else:
            user.email = session['email']
            user.phone_number = session['phone_number']

        user.save()
        del session
        del otp


def check_delay(request):
    now = datetime.now()

    if 'last_try' in request.session:
        str_time = request.session['delay']['time']
        last_try = datetime.strptime(str_time, '%Y-%m-%d %H:%M:%S')
    else:
        last_try = now

    if last_try <= now:
        delay = now + timedelta(minutes=3)
        request.session['delay'] = {
            'time': delay.strftime('%Y-%m-%d %H:%M:%S'),
        }
        return True

    time_left = last_try - now
    total_seconds = int(time_left.total_seconds())
    return False, total_seconds


class UserRegisterView(SuccessMessageMixin, CreateView):
    """
    Register form for new user and send to sms verification view.
    """
    form_class = UserCreationForm
    template_name = 'accounts/register.html'
    success_message = "code was send"
    success_url = reverse_lazy('auth:verify')

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            messages.info(request, 'you already registered')
            return redirect('items:all_items')
        return super().dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        cd = form.cleaned_data

        self.request.session['user_info'] = {
            'register': True,
            'username': cd['username'],
            'email': cd['email'],
            'password': cd['password'],
            'phone_number': cd['phone_number']
            }

        return super().form_valid(form)


class VerifyView(FormView):
    """
    Verify phone number with otp.
    """
    form_class = OTPForm
    template_name = 'accounts/otp.html'
    success_url = reverse_lazy('items:all_items')

    def form_valid(self, form):
        cd = form.cleaned_data
        user_entered_code = cd['code']

        try:
            if 'user_info' in self.request.session:
                session = self.request.session['user_info']
                update_user(self.request, session, user_entered_code)
            return redirect('auth:profile')

        except OTP.DoesNotExist:
            messages.error(self.request, 'not exists')

        return super().form_valid(form)


class UserLoginView(SuccessMessageMixin, LoginView):
    """
    Login and send success message.
    """
    template_name = 'accounts/login.html'
    success_message = "با موفقیت وارد شدید !"
    next_page = reverse_lazy('items:all_items')


class UserProfileView(LoginRequiredMixin, DetailView, UpdateView):
    """
    Show and change user info.
    """
    model = User
    form_class = ProfileForm
    template_name = 'accounts/profile.html'
    success_url = reverse_lazy('auth:profile')
    context_object_name = 'user'
# encode and decode the time

    def form_valid(self, form):
        cd = form.cleaned_data
        delay = check_delay(self.request)
        if form.has_changed() and delay is True:
            changed_fields = form.changed_data

            if len(changed_fields) > 1:
                form.add_error(None, 'cant change 2 fild at same time bitch')
                return self.form_invalid(form)

            if 'username' not in changed_fields:
                send_otp(self.request.user, changed_fields[0])

                self.request.session['user_info'] = {
                    'username': cd['username'],
                    'email': cd['email'],
                    'phone_number': cd['phone_number']
                }
                return redirect('auth:verify')

        else:
            form.add_error(None, f"try after {delay[1]} ")
            return self.form_invalid(form)

        return super().form_valid(form)

    def get_object(self, queryset=None):
        obj = User.objects.get(email__exact=self.request.user.email)
        return obj

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        user_orders = Order.objects.filter(user__exact=self.request.user)
        user_carts = Cart.objects.get(user__exact=self.request.user)

        context['user_orders'] = user_orders
        context['user_carts'] = user_carts

        return context
