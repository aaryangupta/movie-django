from django.contrib import admin
from django.urls import path, include

admin.site.site_header = "Movie Booking Admin Dashboard"
admin.site.site_title = "Movie Booking Admin"
admin.site.index_title = "Welcome to the Admin Dashboard"

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('movies.urls')),
]

