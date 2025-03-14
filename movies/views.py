import random
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm
from .forms import BookingForm, UserRegistrationForm, PaymentForm, ReviewForm
from .api import search_movies, get_movie_details
from .models import Booking, Review

def movie_list(request):
    raw_query = request.GET.get('q', '').strip()
    price_per_ticket = 20  
    if raw_query:
        query = raw_query
    else:
        possible_queries = [
            "star", "love", "life", "war", "man", "girl",
            "dark", "new", "old", "king", "queen", "action",
            "comedy", "drama", "thriller", "sci-fi"
        ]
        query = random.choice(possible_queries)
    movies = search_movies(query, count=25)
    return render(request, 'movies/movie_list.html', {
        'movies': movies,
        'price_per_ticket': price_per_ticket,
        'search_query': raw_query,
        'current_query': query,
    })

def movie_detail(request, imdb_id):
    
    movie = get_movie_details(imdb_id)
    price_per_ticket = 20
    
    reviews = Review.objects.filter(movie_imdb_id=imdb_id).order_by('-created_at')
    
    user_review = None
    if request.user.is_authenticated:
        user_review = Review.objects.filter(movie_imdb_id=imdb_id, user=request.user).first()
    
    if request.method == 'POST':
        if not request.user.is_authenticated:
            return redirect('login')
        
        if user_review:
            form = ReviewForm(request.POST, instance=user_review)
        else:
            form = ReviewForm(request.POST)
        if form.is_valid():
            new_review = form.save(commit=False)
            new_review.user = request.user
            new_review.movie_imdb_id = imdb_id
            new_review.save()
            return redirect('movie_detail', imdb_id=imdb_id)
    else:
        if user_review:
            form = ReviewForm(instance=user_review)
        else:
            form = ReviewForm()
    
    return render(request, 'movies/movie_detail.html', {
        'movie': movie,
        'price_per_ticket': price_per_ticket,
        'reviews': reviews,
        'form': form,
        'user_review': user_review,
    })

def signup(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('movie_list')
    else:
        form = UserRegistrationForm()
    return render(request, 'movies/signup.html', {'form': form})

def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('movie_list')
    else:
        form = AuthenticationForm()
    return render(request, 'movies/login.html', {'form': form})

def logout_view(request):
    logout(request)
    return redirect('movie_list')

def book_ticket(request, movie_title):
    if not request.user.is_authenticated:
        return redirect('login')
    if request.method == 'POST':
        form = BookingForm(request.POST)
        if form.is_valid():
            booking = form.save(commit=False)
            booking.user = request.user
            booking.movie_title = movie_title
            booking.save()
            return redirect('payment', booking_id=booking.id)
    else:
        form = BookingForm()
    return render(request, 'movies/book_ticket.html', {
        'form': form,
        'movie_title': movie_title,
    })

def payment_view(request, booking_id):
    booking = get_object_or_404(Booking, id=booking_id)
    price_per_ticket = 20  # Updated: 20 Euros per ticket
    total_amount = booking.seats * price_per_ticket

    if request.method == 'POST':
        form = PaymentForm(request.POST)
        if form.is_valid():
            method = form.cleaned_data['payment_method']
            if method == 'upi':
                upi_id = form.cleaned_data['upi_id']
                if not upi_id:
                    form.add_error('upi_id', "Please enter your UPI ID for UPI payment method.")
                    return render(request, 'movies/payment.html', {
                        'booking': booking,
                        'price_per_ticket': price_per_ticket,
                        'total_amount': total_amount,
                        'form': form,
                    })
            elif method == 'qr':
                # Dummy processing for QR payment (assume payment via QR)
                pass
            return redirect('payment_confirmation', booking_id=booking.id)
    else:
        form = PaymentForm()

    return render(request, 'movies/payment.html', {
        'booking': booking,
        'price_per_ticket': price_per_ticket,
        'total_amount': total_amount,
        'form': form,
    })

def payment_confirmation_view(request, booking_id):
    booking = get_object_or_404(Booking, id=booking_id)
    price_per_ticket = 20
    total_amount = booking.seats * price_per_ticket
    return render(request, 'movies/payment_confirmation.html', {
        'booking': booking,
        'price_per_ticket': price_per_ticket,
        'total_amount': total_amount,
    })

@login_required
def delete_review(request, review_id):
    review = get_object_or_404(Review, id=review_id, user=request.user)
    imdb_id = review.movie_imdb_id
    if request.method == 'POST':
        review.delete()
    return redirect('movie_detail', imdb_id=imdb_id)
