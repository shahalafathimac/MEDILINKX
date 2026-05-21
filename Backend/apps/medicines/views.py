from django.shortcuts import render
from apps.accounts.permissions import IsSupplier
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from .models import Medicine
from .serializers import MedicineSerializer
from django.db.models import F
# Create your views here.

class MedicineCreateView(APIView):

    permission_classes = [IsAuthenticated, IsSupplier]

    def post(self, request):

        serializer = MedicineSerializer(data=request.data)

        if serializer.is_valid():

            serializer.save(supplier=request.user)

            return Response(
                serializer.data,
                status=status.HTTP_201_CREATED
            )

        return Response(
            serializer.errors,
            status=status.HTTP_400_BAD_REQUEST
        )


class MedicineListView(APIView):

    permission_classes = [IsAuthenticated]

    def get(self, request):

        medicines = Medicine.objects.filter(
            stock_quantity__gt=0
        )

        serializer = MedicineSerializer(
            medicines,
            many=True
        )

        return Response(serializer.data)


class MedicineUpdateView(APIView):

    permission_classes = [IsAuthenticated, IsSupplier]

    def put(self, request, pk):

        try:

            medicine = Medicine.objects.get(
                pk=pk,
                supplier=request.user
            )

        except Medicine.DoesNotExist:

            return Response(
                {"message": "Medicine not found"},
                status=status.HTTP_404_NOT_FOUND
            )

        serializer = MedicineSerializer(
            medicine,
            data=request.data
        )

        if serializer.is_valid():

            serializer.save()

            return Response(serializer.data)

        return Response(
            serializer.errors,
            status=status.HTTP_400_BAD_REQUEST
        )




class MedicineDeleteView(APIView):

    permission_classes = [IsAuthenticated, IsSupplier]

    def delete(self, request, pk):

        try:

            medicine = Medicine.objects.get(
                pk=pk,
                supplier=request.user
            )

        except Medicine.DoesNotExist:

            return Response(
                {"message": "Medicine not found"},
                status=status.HTTP_404_NOT_FOUND
            )

        medicine.delete()

        return Response(
            {"message": "Medicine deleted successfully"},
            status=status.HTTP_200_OK
        )



class LowStockMedicineView(APIView):

    permission_classes = [IsAuthenticated, IsSupplier]

    def get(self, request):

        medicines = Medicine.objects.filter(
            supplier=request.user,
            stock_quantity__lte=F('low_stock_threshold')
        )

        serializer = MedicineSerializer(
            medicines,
            many=True
        )

        return Response(serializer.data)