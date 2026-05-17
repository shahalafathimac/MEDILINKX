from django.urls import path
from .views import RegisterView
from .views import VerifyOTPView
from .views import login_view
from .views import profile_view
urlpatterns = [
    path("register/", RegisterView.as_view()),
    path("verify-otp/", VerifyOTPView.as_view()),
    path('login/', login_view),
    path('profile/', profile_view),
]