
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404
from django.shortcuts import redirect


from mainapp.models import (Hotel, Room, Regions,
                            ListOfCountries, Booking, Review)
from mainapp.forms import RoomForm, HotelForm, RegionForm, ListOfCountriesForm, ReviewForm, BookingForm

from django.core.exceptions import ValidationError




# Главная

def main(request):
    countries = ListOfCountries.objects.filter(is_active=True).prefetch_related(
        'regions__hotels') # выбираются все активные страны из таблицы ListOfCountries, потом регионы этих стран и отели этих регионов

    return render(request, "mainapp/index.html", {'countries': countries})


# Страны
def country_list(request):
    countries = ListOfCountries.objects.all()
    return render(request, 'mainapp/country/country_list.html', {'countries': countries})


# Регионы
def regions_list(request):
    regions = Regions.objects.select_related('country').all()
    return render(request, 'mainapp/region/region_list.html', {'regions': regions})


# Отели
def hotel_list(request):
    hotels = Hotel.objects.filter(deleted=False, is_active=True)
    return render(request, "mainapp/hotel/hotel_list.html", {"hotels": hotels})


def hotel_detail(request, pk):
    hotel = get_object_or_404(Hotel, pk=pk, deleted=False)
    rooms = Room.objects.filter(hotel=hotel, deleted=False)
    return render(request, "mainapp/hotel/hotel_detail.html", {
        "hotel": hotel,
        "rooms": rooms
    })


# Rooms
def room_list(request, hotel_id):
    rooms = Room.objects.filter(hotel_id=hotel_id, deleted=False)
    return render(request, "mainapp/room/room_list.html", {"rooms": rooms, "hotel_id": hotel_id})


def room_detail(request, pk):
    room = get_object_or_404(Room, pk=pk, deleted=False)
    return render(request, "mainapp/room/room_detail.html", {"room": room})


# Создание бронирования
@login_required
def booking_create(request):
    room_id = request.GET.get('room')

    if request.method == 'POST':
        form = BookingForm(request.POST)
        if form.is_valid():
            booking = form.save(commit=False)
            booking.user = request.user

            # Здесь вставляем проверку через full_clean()
            try:
                booking.full_clean()  # вызывает clean() модели
                booking.save()  # только если ошибок нет
            except ValidationError as e:
                form.add_error(None, e)
                return render(request, 'mainapp/booking/booking_form.html', {'form': form})

            return redirect('mainapp:booking_list')
    else:
        initial = {}
        if room_id:
            initial['room'] = room_id
        form = BookingForm(initial=initial)

    return render(request, 'mainapp/booking/booking_form.html', {'form': form})


# Список бронирований текущего пользователя
@login_required
def booking_list(request):
    bookings = Booking.objects.filter(
        user=request.user,
        deleted=False,
        in_order=False
    ).order_by('-created')

    return render(request, 'mainapp/booking/booking_list.html', {
        'bookings': bookings
    })


# Создание отзыва
def hotel_reviews(request, hotel_id):
    hotel = get_object_or_404(Hotel, id=hotel_id)
    reviews = Review.objects.filter(hotel=hotel).order_by('-created')
    return render(request, 'mainapp/hotel_reviews.html', {
        'hotel': hotel,
        'reviews': reviews
    })


@login_required
def review_create(request, hotel_id):
    hotel = get_object_or_404(Hotel, id=hotel_id, is_active=True)
    if request.method == 'POST':
        form = ReviewForm(request.POST)
        if form.is_valid():
            review = form.save(commit=False)
            review.user = request.user
            review.hotel = hotel
            review.save()
            return redirect('mainapp:hotel_detail', pk=hotel.id)
    else:
        form = ReviewForm(initial={'hotel': hotel})
    return render(request, 'mainapp/review_form.html', {'form': form, 'hotel': hotel})


