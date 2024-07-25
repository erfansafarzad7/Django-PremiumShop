from django.db import models
from django.utils.translation import gettext_lazy as _


class Category(models.Model):
    title = models.CharField(_("نام دسته بندی"), max_length=50)
    created_date = models.DateTimeField(_("تاریخ ایجاد"), auto_now_add=True)

    class Meta:
        verbose_name = 'دسته بندی'
        verbose_name_plural = 'دسته بندی ها'

    def __str__(self):
        return self.title


class Variables(models.Model):
    key = models.CharField(_("مقدار"), max_length=50)
    price = models.PositiveIntegerField(_("قیمت"), )
    discount = models.PositiveSmallIntegerField(_("درصد تخفیف"))

    class Meta:
        verbose_name = 'متغیر'
        verbose_name_plural = 'متغیر ها'

    def __str__(self):
        return f'{self.key} - {self.price}'


class Choices(models.Model):
    title = models.CharField(_("موضوع"), max_length=50)
    choices = models.ManyToManyField(Variables, related_name="choices_value")

    class Meta:
        verbose_name = 'موارد'
        verbose_name_plural = 'موارد'

    def __str__(self):
        return self.title


class Item(models.Model):
    image = models.ImageField(_("عکس"), null=True, blank=True)
    title = models.CharField(_("عنوان"), max_length=150, unique=True)
    description = models.TextField(_("توضیحات"), )
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='item_category', verbose_name="دسته بندی")
    choices = models.ManyToManyField(Choices, related_name='item_choices')

    created_date = models.DateTimeField(_("تاریخ ایجاد"), auto_now_add=True)
    updated_date = models.DateTimeField(_("تاریخ آپدیت"), auto_now=True)

    class Meta:
        verbose_name = 'آیتم'
        verbose_name_plural = 'آیتم ها'

    def __str__(self):
        return self.title

    # @property
    # def discounted_price(self):
    #     return int(self.price * (1 - self.discount / 100)) if self.discount else self.price
