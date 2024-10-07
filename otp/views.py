import requests
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
import random
from .models import OTP
from django.core.mail import send_mail

class SendOTPView(APIView):
    def post(self, request):
        email = request.data.get('email')  # Get email if provided
        phoneNumber = request.data.get('phoneNumber')  # Get phone number if provided

        # Generate OTP
        otp = str(random.randint(100000, 999999))

        # Fast2SMS API credentials
        api_key = "atKN10DEJ7yBW8pOH2F95zbAvdjkImXPhRconr6ZMwGSQsY4xTKmXsFILBkYHE2495gRCvSidW8zDPef"
        url = "https://www.fast2sms.com/dev/bulkV2"

        # Check if email is provided
        if email:
            OTP.objects.create(email=email, otp=otp)  # Save OTP for email

            # Send OTP via email
            send_mail(
                'Your OTP Code',
                f'Your OTP is {otp}',
                'your_email@gmail.com',  # Replace with your sender email
                [email],
                fail_silently=False,
            )

            return Response({"message": "OTP sent successfully to your email.", "email": email, "otp": otp}, status=status.HTTP_200_OK)

        # Check if phone number is provided
        elif phoneNumber:
            # Ensure the phone number starts with '+91' for India
            if not phoneNumber.startswith('+91'):
                phoneNumber = '+91' + phoneNumber  # Automatically prepend country code

            # Save OTP for phone number
            OTP.objects.create(phone_number=phoneNumber, otp=otp)

            # Send OTP via Fast2SMS
            params = {
                'authorization': api_key,
                'route': 'otp',
                'variables_values': otp,
                'numbers': phoneNumber,
                'flash': '0',
            }

            response = requests.get(url, params=params)

            if response.status_code == 200:
                return Response({"message": "OTP sent successfully to your phone number", "phone_number": phoneNumber, "otp": otp}, status=status.HTTP_200_OK)
            else:
                return Response({"error": "Failed to send OTP via Fast2SMS."}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        # If neither email nor phone number is provided
        return Response({"error": "Either email or phone number is required."}, status=status.HTTP_400_BAD_REQUEST)
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import OTP
from twilio.rest import Client
from django.core.mail import send_mail
import random

class SendOTPView(APIView):
    def post(self, request):
        email = request.data.get('email')  # Get email if provided
        phoneNumber = request.data.get('phoneNumber')  # Get phone number if provided
        
        # Generate OTP (for local storage/testing purposes)
        otp = str(random.randint(100000, 999999))

        # Twilio credentials
        account_sid = 'ACf797cb12d7e73d19a2f8c9d1152ebd56'  # Your Account SID
        auth_token = '7e44060f451cfb9fda41c481127f5340'  # Your Auth Token
        service_id = 'VA4ff870dcd03db9632450ef24e64b376b'  # Your Service ID
        client = Client(account_sid, auth_token)

        # Check if email is provided
        if email:
            # Handle email case
            OTP.objects.create(email=email, otp=otp)  # Save OTP for email

            # Send OTP via email
            send_mail(
                'Your OTP Code',
                f'Your OTP is {otp}',
                'your_email@gmail.com',  # Replace with your sender email
                [email],
                fail_silently=False,
            )

            return Response({"message": "OTP sent successfully to your email.", "email": email, "otp": otp}, status=status.HTTP_200_OK)

        # Check if phone number is provided
        elif phoneNumber:
            # Ensure the phone number starts with '+91' for India
            if not phoneNumber.startswith('+91'):
                phoneNumber = '+91' + phoneNumber  # Automatically prepend country code

            # Handle phone number case
            OTP.objects.create(phone_number=phoneNumber, otp=otp)  # Save OTP for phone (testing purposes)

            # Send OTP via Twilio Verify
            verification = client.verify \
                .v2 \
                .services(service_id) \
                .verifications \
                .create(to=phoneNumber, channel='sms')

            print(f"Verification SID: {verification.sid}")  # For logging purposes

            # In development, return the OTP
            return Response({"message": "OTP sent successfully to your phone number", "phone_number": phoneNumber, "otp": otp}, status=status.HTTP_200_OK)

        # If neither email nor phone number is provided
        return Response({"error": "Either email or phone number is required."}, status=status.HTTP_400_BAD_REQUEST)
