from django.urls import path,include
from . import views

app_name = "tickets"

urlpatterns = [
    path('new-ticket/', views.TicketView.as_view(),name="send"),
    path('my-tickets/', views.MyTicketView.as_view(),name="all"),
]
