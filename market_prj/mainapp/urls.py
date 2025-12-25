from django.urls import path
from mainapp import views, api_views



app_name = 'mainapp'

urlpatterns = [
    path('', views.main, name='main'),

    path("countries/", views.country_list, name="countries_list"),
    path("regions/", views.regions_list, name="regions_list"),

    path("hotels/", views.hotel_list, name="hotel_list"),
    path("hotels/<int:pk>/", views.hotel_detail, name="hotel_detail"),

    path("hotels/<int:hotel_id>/rooms/", views.room_list, name="room_list"),

    path("rooms/<int:pk>/", views.room_detail, name="room_detail"),

    path("bookings/", views.booking_list, name="booking_list"),  # Список бронирований текущего пользователя
    path("booking/create/", views.booking_create, name="booking_create"),  # Создать бронирование

    #path("hotels/<int:hotel_id>/review/", views.review_create, name="review_create"),

    path('hotel/<int:hotel_id>/reviews/', views.hotel_reviews, name='hotel_reviews'),
    path("hotels/<int:hotel_id>/review/", views.review_create, name="review_create"), # Создать отзыв для отеля

    path('api/hotels/', api_views.api_hotels, name='api_hotels'),
    path('api/hotel/<int:hotel_id>/review', api_views.api_hotels_review, name='api_hotels_review'),
]
