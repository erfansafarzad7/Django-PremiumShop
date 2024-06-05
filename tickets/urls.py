from django.urls import path,include
from . import views

app_name = "tickets"

urlpatterns = [
    path('', views.TicketView.as_view(),name="all"),
]
