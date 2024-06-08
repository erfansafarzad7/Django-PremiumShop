from django.db import models
from django.dispatch import receiver
from django.db.models.signals import post_save


STATUS_CHOICES = (
    ('Sent', 'Sent'),
    ('Answered', 'Answered'),
)


class Ticket(models.Model):
    status = models.CharField(max_length=10, choices=STATUS_CHOICES)
    user = models.ForeignKey('accounts.User', on_delete=models.CASCADE, related_name='user_ticket')
    title = models.CharField(max_length=30)
    text = models.TextField()
    response = models.TextField(null=True, blank=True)

    created_date = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    updated_date = models.DateTimeField(auto_now=True, null=True, blank=True)

    def __str__(self):
        return f"{self.user} - {self.title}"


@receiver(post_save, sender=Ticket)
def create_profile(sender, instance, created, **kwargs):
    if created:
        print(instance.text)
