import datetime

from django import forms
from django.core.exceptions import ValidationError

from orders.models import Coupon


class CouponForm(forms.Form):
    code = forms.CharField(max_length=30)

    def clean_coupon(self):
        coupon_code = self.cleaned_data['code']

        try:
            coupon = Coupon.objects.get(code__exact=coupon_code)

            if c := coupon.coupon_validity_time:
                if c < datetime.datetime.now():
                    raise ValidationError('کد تخفیف منقضی شده است!')

        except Coupon.DoesNotExist:
            raise ValidationError('کد تخفیف اشتباه است!')

        return coupon_code
