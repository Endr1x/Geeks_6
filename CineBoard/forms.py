from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import get_user_model
from .models import Movie, Comment, VipSeatBooking

User = get_user_model()

class MovieForm(forms.ModelForm):
    class Meta:
        model = Movie
        fields = '__all__'
        widgets = {
            'release_date': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
        }

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['text']
        widgets = {
            'text': forms.Textarea(attrs={'rows': 3, 'class': 'form-control', 'placeholder': 'Оставьте ваш отзыв...'})
        }

class VipBookingForm(forms.ModelForm):
    class Meta:
        model = VipSeatBooking
        fields = ['seat_number']
        widgets = {
            'seat_number': forms.NumberInput(attrs={'class': 'form-control', 'min': 1, 'max': 50})
        }

class CustomUserRegisterForm(UserCreationForm):
    class Meta:
        model = User
        fields = ('username', 'email')
