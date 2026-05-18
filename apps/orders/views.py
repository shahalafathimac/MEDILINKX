from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from .models import Order
from .serializers import OrderSerializer
from apps.accounts.permissions import IsBuyer, IsSupplier
from apps.medicines.models import Medicine

# Create your views here.

class PlaceOrderView(APIView):

    permission_classes = [IsAuthenticated, IsBuyer]

    def post(self, request):
        medicine_id = request.data.get('medicine')
        quantity = int(request.data.get('quantity'))
        try:
            medicine = Medicine.objects.get(
                id=medicine_id
            )
        except Medicine.DoesNotExist:
            return Response(
                {"message": "Medicine not found"},
                status=status.HTTP_404_NOT_FOUND
            )

        # STOCK CHECK
        if quantity > medicine.stock_quantity:
            return Response(
                {"message": "Insufficient stock"},
                status=status.HTTP_400_BAD_REQUEST
            )
        total_price = quantity * medicine.price
        order = Order.objects.create(
            buyer=request.user,
            medicine=medicine,
            quantity=quantity,
            total_price=total_price
        )

        # REDUCE STOCK
        medicine.stock_quantity -= quantity
        medicine.save()
        serializer = OrderSerializer(order)
        return Response(
            serializer.data,
            status=status.HTTP_201_CREATED
        )




class SupplierOrdersView(APIView):

    permission_classes = [IsAuthenticated, IsSupplier]

    def get(self, request):

        orders = Order.objects.filter(
            medicine__supplier=request.user
        )

        serializer = OrderSerializer(
            orders,
            many=True
        )

        return Response(serializer.data)




class UpdateOrderStatusView(APIView):

    permission_classes = [IsAuthenticated, IsSupplier]

    def put(self, request, pk):

        try:

            order = Order.objects.get(
                pk=pk,
                medicine__supplier=request.user
            )

        except Order.DoesNotExist:

            return Response(
                {"message": "Order not found"},
                status=status.HTTP_404_NOT_FOUND
            )

        new_status = request.data.get('status')

        order.status = new_status

        order.save()

        serializer = OrderSerializer(order)

        return Response(serializer.data)