from django import forms
from .models import Movie, Comment, VIPBooking

class MovieForm(forms.ModelForm):
    class Meta:
        model = Movie
        fields = [
            'title', 'description', 'release_year', 'director',
            'country', 'duration_minutes', 'age_rating', 'rating',
            'poster', 'genres'
        ]
        widgets = {
            'genres': forms.CheckboxSelectMultiple(),
        }

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['text']
        widgets = {
            'text': forms.Textarea(attrs={'rows': 3, 'placeholder': 'Напишите отзыв...'}),
        }

class VIPBookingForm(forms.ModelForm):
    class Meta:
        model = VIPBooking
        fields = ['seat_number']
