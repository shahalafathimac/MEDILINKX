from rest_framework.views import APIView
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from datetime import timedelta
from .serializers import VerifyOTPSerializer
from .serializers import RegisterSerializer
from .utils import generate_otp, send_otp_email
from .models import OTP,User
from django.utils import timezone
from django.contrib.auth import authenticate
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import permission_classes
from .permissions import IsSupplier, IsBuyer, IsAdmin

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




@api_view(['POST'])
def login_view(request):

    email = request.data.get('email')
    password = request.data.get('password')

    try:
        user = User.objects.get(email=email)

    except User.DoesNotExist:

        return Response({
            'message': 'User not found'
        }, status=status.HTTP_404_NOT_FOUND)

    if not user.is_verified:

        return Response({
            'message': 'Email not verified'
        }, status=status.HTTP_400_BAD_REQUEST)

    if not user.is_approved:

        return Response({
            'message': 'Admin approval pending'
        }, status=status.HTTP_400_BAD_REQUEST)

    user = authenticate(
        username=user.username,
        password=password
    )

    if user is None:

        return Response({
            'message': 'Invalid credentials'
        }, status=status.HTTP_401_UNAUTHORIZED)

    
    # created the JWT tokens
    refresh = RefreshToken.for_user(user)

    return Response({

        'message': 'Login successful',

        'access_token': str(refresh.access_token),

        'refresh_token': str(refresh),
    })




@api_view(['GET'])

@permission_classes([IsAuthenticated])

def profile_view(request):

    return Response({

        'message': 'Profile accessed',

        'email': request.user.email
    })



class SupplierDashboardView(APIView):

    permission_classes = [IsAuthenticated, IsSupplier]

    def get(self, request):

        return Response({
            "message": "Welcome Supplier Dashboard"
        })

class BuyerDashboardView(APIView):

    permission_classes = [IsAuthenticated, IsBuyer]

    def get(self, request):

        return Response({
            "message": "Welcome Buyer Dashboard"
        })

class AdminDashboardView(APIView):

    permission_classes = [IsAuthenticated, IsAdmin]

    def get(self, request):

        return Response({
            "message": "Welcome Admin Dashboard"
        })