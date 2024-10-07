# models.py
from django.db import models
import random

class OTP(models.Model):
    email = models.EmailField(null=True, blank=True)  # Field for email OTPs
    phone_number = models.CharField(max_length=15, null=True, blank=True)  # Field for phone number OTPs
    otp = models.CharField(max_length=6)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"OTP for {self.email or self.phone_number}: {self.otp}"

    @staticmethod
    def generate_otp():
        return str(random.randint(100000, 999999))
