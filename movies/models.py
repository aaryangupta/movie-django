from django.db import models
from django.contrib.auth.models import User

class Booking(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    movie_title = models.CharField(max_length=200)
    seats = models.IntegerField()
    booking_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} - {self.movie_title}"

class Review(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    movie_imdb_id = models.CharField(max_length=20)  # Example: "tt1234567"
    rating = models.PositiveIntegerField(default=1)  # Rating range (1-5)
    comment = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Review by {self.user.username} for {self.movie_imdb_id}"
