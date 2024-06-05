from django.urls import path,include
from . import views

app_name = "orders"

urlpatterns = [
    path('add-to-cart/<int:item_id>/',views.AddToCartsView.as_view(),name="add_to_cart"),
    path('delete-cart-item/<int:item_id>/',views.DeleteCartView.as_view(),name="delete_cart"),
    path('create-order/',views.CreateOrderView.as_view(),name="create_order"),
    path('order-detail/<int:order_code>/',views.OrderDetailView.as_view(),name="order_detail"),
    path('cancel-order/<str:order_code>/',views.CancelOrderView.as_view(),name="cancel_order"),
    path('pay-order/<str:order_code>/',views.PayOrderView.as_view(),name="pay_order"),

]
