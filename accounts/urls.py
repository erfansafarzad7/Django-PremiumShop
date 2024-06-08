from django.urls import path,include
from django.contrib.auth.views import LogoutView
from . import views

app_name = "auth"

urlpatterns = [
    path('register/', views.UserRegisterView.as_view(), name="register"),
    path('login/', views.UserLoginView.as_view(), name="login"),
    path('logout/', LogoutView.as_view(), name="logout"),
    path('verify/', views.VerifyView.as_view(), name='verify'),
    path('forget-password/', views.ForgetPasswordView.as_view(), name='forget_password'),
    path('profile/', views.UserProfileView.as_view(), name='profile'),
]
