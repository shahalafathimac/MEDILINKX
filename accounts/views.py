from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from datetime import timedelta
from .serializers import VerifyOTPSerializer
from .serializers import RegisterSerializer
from .utils import generate_otp, send_otp_email
from .models import OTP,User
from django.utils import timezone

class RegisterView(APIView):

    def post(self, request):

        serializer = RegisterSerializer(data=request.data)

        if serializer.is_valid():
            user = serializer.save()
            otp = generate_otp()

            # SAVE OTP IN DATABASE
            OTP.objects.create(
                user=user,
                otp=otp
            )
            send_otp_email(user.email, otp)

            return Response({
                "message": "User registered successfully"
            })

        return Response(serializer.errors)



class VerifyOTPView(APIView):

    def post(self, request):

        serializer = VerifyOTPSerializer(data=request.data)

        if serializer.is_valid():

            email = serializer.validated_data['email']

            otp = serializer.validated_data['otp']

            try:

                user = User.objects.get(email=email)

            except User.DoesNotExist:

                return Response(
                    {"message": "User not found"},
                    status=status.HTTP_404_NOT_FOUND
                )

            try:

                otp_obj = OTP.objects.filter(
                    user=user,
                    otp=otp,
                    is_used=False
                ).latest('created_at')

            except OTP.DoesNotExist:

                return Response(
                    {"message": "Invalid OTP"},
                    status=status.HTTP_400_BAD_REQUEST
                )

            expiry_time = otp_obj.created_at + timedelta(minutes=5)

            if timezone.now() > expiry_time:

                return Response(
                    {"message": "OTP expired"},
                    status=status.HTTP_400_BAD_REQUEST
                )

            user.is_verified = True

            user.save()

            otp_obj.is_used = True

            otp_obj.save()

            return Response(
                {"message": "OTP verified successfully"},
                status=status.HTTP_200_OK
            )

        return Response(serializer.errors)