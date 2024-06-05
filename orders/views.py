from django.urls import reverse
from django.shortcuts import redirect
from django.views.generic import ListView, FormView, RedirectView, TemplateView, DetailView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from items.models import Item
from .models import Cart, Order

import random


class AddToCartsView(LoginRequiredMixin, RedirectView):
    # get item id and create session carts redirect to user profile

    def get_redirect_url(self, *args, **kwargs):
        return reverse('auth:profile')

    def get(self, request, *args, **kwargs):
        item_id = self.kwargs['item_id']
        item = Item.objects.filter(id__exact=item_id)
        try:
            cart = Cart.objects.get(user__exact=self.request.user)
            # get, create = CartItem.objects.get_or_create(item=item, quantity=1, total_price=item.discounted_price)
            cart.items.add(item[0].id)
            cart.save()
        except Cart.DoesNotExist:
            print('cart nist')

        return super().get(self, request, *args, **kwargs)


class DeleteCartView(LoginRequiredMixin, RedirectView):
    def get_redirect_url(self, *args, **kwargs):
        return reverse('auth:profile')

    def get(self, request, *args, **kwargs):
        item_id = self.kwargs['item_id']
        item = Item.objects.filter(id__exact=item_id)
        try:
            cart = Cart.objects.get(user__exact=self.request.user)
            # get, create = CartItem.objects.get_or_create(item=item, quantity=1, total_price=item.discounted_price)
            cart.items.remove(item[0].id)
            cart.save()
        except Cart.DoesNotExist:
            print('cart nist')

        return super().get(self, request, *args, **kwargs)


class CreateOrderView(LoginRequiredMixin, RedirectView):
    # check user is verify and has phone number - create order/default accepted and send to pay

    def get_redirect_url(self, *args, **kwargs):
        return reverse('auth:profile')

    def get(self, request, *args, **kwargs):

        # cart_id = self.kwargs['cart_id']
        user = request.user
        cart = Cart.objects.get(user__exact=user)
        if user.is_verified and user.phone_number:
            random_code = str(random.randint(1000000000, 9999999999))
            order = Order.objects.create(code=random_code, user=user, status='On pay')
            # order.calculate_total_price()
            for i in cart.items.all():
                order.items.add(i.id)
            cart.items.clear()
            order.save()

        else:
            messages.warning(request, 'verify phone number')

        return super().get(self, request, *args, **kwargs)


class OrderDetailView(DetailView):
    model = Order
    template_name = 'orders/order_detail.html'
    context_object_name = 'order'

    def get_object(self, queryset=None):
        order_code = self.kwargs['order_code']
        order = Order.objects.get(code__exact=order_code)
        return order


class CancelOrderView(LoginRequiredMixin, RedirectView):
    # get order id and set to cancelled redirect to user profile
    def get_redirect_url(self, *args, **kwargs):
        return reverse('auth:profile')

    def get(self, request, *args, **kwargs):
        order_code = self.kwargs['order_code']
        try:
            order = Order.objects.get(code__exact=order_code)
            order.status = 'Cancelled'
            order.save()
        except Order.DoesNotExist:
            messages.warning(request, 'order not found')
            return redirect('auth:profile')

        return super().get(self, request, *args, **kwargs)


class PayOrderView(LoginRequiredMixin, TemplateView):
    # get order id and set to Paid/True/in_progress   redirect to user profile
    template_name = 'orders/order_pay.html'


