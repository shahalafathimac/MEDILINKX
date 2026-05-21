from django.urls import path
from .views import (RegisterView,
                    login_view,
                    profile_view,
                    SupplierDashboardView,
                    BuyerDashboardView,
                    AdminDashboardView,
                    SetupMFAView,
                    VerifyMFAView,
                    verify_login_mfa)

urlpatterns = [
    path("register/", RegisterView.as_view()),
    path("login/", login_view),
    path("profile/", profile_view),
    path('supplier/dashboard/',SupplierDashboardView.as_view()),
    path('buyer/dashboard/',BuyerDashboardView.as_view()),
    path('admin/dashboard/',AdminDashboardView.as_view()),
    path('setup-mfa/',SetupMFAView.as_view()),
    path('verify-mfa/',VerifyMFAView.as_view()),
    path('verify-login-mfa/',verify_login_mfa),
]