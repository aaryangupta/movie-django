from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Booking, Review

class UserRegistrationForm(UserCreationForm):
    email = forms.EmailField(required=True)
    
    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']

class BookingForm(forms.ModelForm):
    class Meta:
        model = Booking
        fields = ['seats']

class ReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = ['rating', 'comment']
        labels = {
            'rating': 'Your Rating (1-5)',
            'comment': 'Your Review',
        }

class PaymentForm(forms.Form):
    PAYMENT_METHOD_CHOICES = [
        ('qr', 'Pay by Scanning QR Code'),
        ('upi', 'Pay via UPI ID'),
    ]
    payment_method = forms.ChoiceField(
        choices=PAYMENT_METHOD_CHOICES,
        widget=forms.RadioSelect,
        label="Payment Method"
    )
    upi_id = forms.CharField(
        label='Enter your UPI ID',
        max_length=50,
        required=False
    )
