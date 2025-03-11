from django.urls import path
from . import views

urlpatterns = [
    path('', views.movie_list, name='movie_list'),
    path('movie/<str:imdb_id>/', views.movie_detail, name='movie_detail'),
    path('signup/', views.signup, name='signup'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('book/<str:movie_title>/', views.book_ticket, name='book_ticket'),
    path('payment/<int:booking_id>/', views.payment_view, name='payment'),
    path('payment_confirmation/<int:booking_id>/', views.payment_confirmation_view, name='payment_confirmation'),
    path('review/delete/<int:review_id>/', views.delete_review, name='delete_review'),

    
]
