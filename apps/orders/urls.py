from django.urls import path
from .views import (PlaceOrderView,SupplierOrdersView,UpdateOrderStatusView)
urlpatterns = [
    path('place/',PlaceOrderView.as_view()),
    path('supplier-orders/',SupplierOrdersView.as_view()),
    path('<int:pk>/update-status/',UpdateOrderStatusView.as_view()),
]