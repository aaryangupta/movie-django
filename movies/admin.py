from django.contrib import admin
from .models import Booking, Review

@admin.register(Booking)
class BookingAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'movie_title', 'seats', 'booking_date')
    search_fields = ('movie_title', 'user__username')
    list_filter = ('booking_date',)
    ordering = ('-booking_date',)

@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'movie_imdb_id', 'rating', 'created_at')
    search_fields = ('movie_imdb_id', 'user__username', 'comment')
    list_filter = ('created_at', 'rating')
    ordering = ('-created_at',)
