from django.contrib import admin
from .models import Movie, Genre, Comment, VIPBooking

admin.site.register(Movie)
admin.site.register(Genre)
admin.site.register(Comment)
admin.site.register(VIPBooking)
