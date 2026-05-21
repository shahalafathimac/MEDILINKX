from django.urls import path

from .views import (MedicineCreateView,MedicineListView,MedicineUpdateView,MedicineDeleteView,LowStockMedicineView,)

urlpatterns = [
    path('',MedicineListView.as_view(),name='medicine-list'),
    path('create/',MedicineCreateView.as_view(),name='medicine-create'),
    path('<int:pk>/update/',MedicineUpdateView.as_view(),name='medicine-update'),
    path('<int:pk>/delete/',MedicineDeleteView.as_view(),name='medicine-delete'),
    path('low-stock/',LowStockMedicineView.as_view(),name='low-stock-medicines'),
]