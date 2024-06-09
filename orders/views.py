from django.urls import reverse, reverse_lazy
from django.shortcuts import redirect
from django.views.generic import ListView, FormView, RedirectView, TemplateView, DetailView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from items.models import Item
from .models import Cart, Order, Coupon
from .forms import CouponForm

import random


class CartsView(LoginRequiredMixin, DetailView, FormView):
    form_class = CouponForm
    model = Cart
    template_name = 'orders/carts.html'
    success_url = reverse_lazy('orders:my_carts')

    def get_object(self, queryset=None):
        return Cart.objects.get(user__exact=self.request.user)

    def form_valid(self, form):
        cd = form.cleaned_data
        coupon_code = cd['code']
        item = self.get_object()
        item.coupon = Coupon.objects.get(code__exact=coupon_code)
        item.save()
        return super().form_valid(form)


class AddToCartsView(LoginRequiredMixin, RedirectView):
    def get_redirect_url(self, *args, **kwargs):
        return reverse('orders:my_carts')

    def get(self, request, *args, **kwargs):
        item_id = self.kwargs['item_id']
        item = Item.objects.get(id__exact=item_id)
        try:
            cart = Cart.objects.get(user__exact=self.request.user)
            cart.items.add(item.id)
            cart.save()
        except Cart.DoesNotExist:
            messages.error(request, 'آیتم مورد نظر یافت نشد')
        return super().get(self, request, *args, **kwargs)


class DeleteCartItemView(LoginRequiredMixin, RedirectView):
    def get_redirect_url(self, *args, **kwargs):
        return reverse('orders:my_carts')

    def get(self, request, *args, **kwargs):
        item_id = self.kwargs['item_id']
        item = Item.objects.filter(id__exact=item_id)
        try:
            cart = Cart.objects.get(user__exact=self.request.user)
            cart.items.remove(item[0].id)
            cart.save()
        except Cart.DoesNotExist:
            messages.error(request, 'آیتم مورد نظر یافت نشد')

        return super().get(self, request, *args, **kwargs)


class DeleteAllCartsView(LoginRequiredMixin, RedirectView):
    def get_redirect_url(self, *args, **kwargs):
        return reverse('orders:my_carts')

    def get(self, request, *args, **kwargs):
        try:
            carts = Cart.objects.get(user__exact=self.request.user)
            carts.items.clear()
        except Cart.DoesNotExist:
            messages.error(request, 'آیتم مورد نظر یافت نشد')

        return super().get(self, request, *args, **kwargs)


class OrdersView(LoginRequiredMixin, ListView):
    model = Order
    template_name = 'orders/orders.html'
    context_object_name = 'orders'

    def get_queryset(self):
        return Order.objects.filter(user__exact=self.request.user)


class CreateOrderView(LoginRequiredMixin, RedirectView):

    def get_redirect_url(self, *args, **kwargs):
        return reverse('orders:my_orders')

    def get(self, request, *args, **kwargs):
        user = request.user
        cart = Cart.objects.get(user__exact=user)

        if user.is_verified and user.phone_number:
            random_code = str(random.randint(1000000000, 9999999999))
            order = Order.objects.create(code=random_code, user=user, status='On Pay')

            order.must_pay = cart.calculate_total_price_with_coupon

            if cart.coupon:
                order.coupon_used = cart.coupon.discount_percent

            for i in cart.items.all():
                order.items.add(i.id)

            cart.coupon = None
            cart.items.clear()
            order.save()
            cart.save()

        else:
            messages.warning(request, 'شماره تلفن خود را ثبت کنید..')
            return redirect('auth:profile')

        return super().get(self, request, *args, **kwargs)


class OrderDetailView(DetailView):
    model = Order
    template_name = 'orders/order_detail.html'
    context_object_name = 'order'

    def get_object(self, queryset=None):
        order_code = self.kwargs['order_code']
        try:
            order = Order.objects.get(code__exact=order_code)
        except Order.DoesNotExist:
            messages.warning(self.request, 'سفارشی یافت نشد..')
            return redirect('orders:my_orders')
        return order


class CancelOrderView(LoginRequiredMixin, RedirectView):
    def get_redirect_url(self, *args, **kwargs):
        return reverse('orders:my_orders')

    def get(self, request, *args, **kwargs):
        order_code = self.kwargs['order_code']
        try:
            order = Order.objects.get(code__exact=order_code)
            order.status = 'Cancelled'
            order.save()
        except Order.DoesNotExist:
            messages.warning(request, 'سفارشی یافت نشد..')
            return redirect('auth:profile')

        return super().get(self, request, *args, **kwargs)


class PayOrderView(LoginRequiredMixin, TemplateView):
    template_name = 'orders/thank-you-page.html'

    def get(self, request, *args, **kwargs):
        order_code = self.kwargs['order_code']
        order = Order.objects.get(code__exact=order_code)
        order.status = 'Paid'
        order.paid = order.must_pay
        order.must_pay = 0
        order.save()
        return super().get(request, *args, **kwargs)


