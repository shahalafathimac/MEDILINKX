from django.shortcuts import render
from rest_framework.views import APIView

from rest_framework.response import Response

from rest_framework.permissions import IsAuthenticated

from apps.medicines.models import Medicine

from apps.orders.models import Order

from apps.accounts.models import User


# Create your views here.



class DashboardView(APIView):

    permission_classes = [IsAuthenticated]

    def get(self, request):

        user = request.user

        data = {

            "username": user.username,

            "email": user.email,

            "role": user.role,
        }

        # ADMIN DASHBOARD
        if user.role == "admin":

            data["total_users"] = User.objects.count()

            data["total_medicines"] = Medicine.objects.count()

            data["total_orders"] = Order.objects.count()

            data["recent_users"] = list(

                User.objects.values(
                    "id",
                    "username",
                    "email",
                    "role"
                )[:5]
            )

        # SUPPLIER DASHBOARD
        elif user.role == "supplier":

            supplier_medicines = Medicine.objects.filter(
                supplier=user
            )

            data["total_medicines"] = supplier_medicines.count()

            data["low_stock"] = supplier_medicines.filter(
                stock__lt=10
            ).count()

            data["recent_medicines"] = list(

                supplier_medicines.values(
                    "id",
                    "name",
                    "stock",
                    "price"
                )[:5]
            )

        # BUYER DASHBOARD
        elif user.role == "buyer":

            data["available_medicines"] = Medicine.objects.count()

            buyer_orders = Order.objects.filter(
                buyer=user
            )

            data["my_orders"] = buyer_orders.count()

            data["recent_orders"] = list(

                buyer_orders.values(
                    "id",
                    "status",
                    "total_price"
                )[:5]
            )

        return Response(data)
