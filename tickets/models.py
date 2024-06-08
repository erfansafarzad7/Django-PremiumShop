from django.db import models
from django.dispatch import receiver
from django.db.models.signals import post_save
from django.core.mail import send_mail
from django.utils.translation import gettext_lazy as _


STATUS_CHOICES = (
    ('Sent', 'ارسال شد'),
    ('Answered', 'پاسخ داده شد'),
)


class Ticket(models.Model):
    status = models.CharField(_("وضعیت"), max_length=10, choices=STATUS_CHOICES)
    user = models.ForeignKey('accounts.User', on_delete=models.CASCADE, related_name='user_ticket', verbose_name="کابر")
    subject = models.CharField(_("موضوع"), max_length=30)
    text = models.TextField(_("متن"), )
    response = models.TextField(_("پاسخ"), null=True, blank=True)

    created_date = models.DateTimeField(_("تاریخ آپدیت"), auto_now_add=True, null=True, blank=True)
    updated_date = models.DateTimeField(_("تاریخ ایجاد"), auto_now=True, null=True, blank=True)

    class Meta:
        verbose_name = 'تیکت'
        verbose_name_plural = 'تیکت ها'

    def __str__(self):
        return f"{self.user} - {self.subject}"


@receiver(post_save, sender=Ticket)
def create_profile(sender, instance, created, **kwargs):
    if created:
        send_mail(
            "New Ticket :",
            f"{instance.user.email} - {instance.subject} - {instance.text}",
            "efi.dragon20002gmail.com",
            ["erfansafarzad7@gmail.com", ]
        )
    else:
        instance.status = 'Answered'
        send_mail(
            "We Answered Your Ticket :",
            f" تیکت شما با موضوع : {instance.subject} ، پاسخ داده شد. ",
            "efi.dragon20002gmail.com",
            [instance.user.email, ]
        )
