from django.urls import path
from .views import RegisterView
from .views import VerifyOTPView

urlpatterns = [
    path("register/", RegisterView.as_view()),
    path("verify-otp/", VerifyOTPView.as_view()),
]