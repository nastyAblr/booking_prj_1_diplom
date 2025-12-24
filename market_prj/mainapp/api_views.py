from rest_framework.decorators import api_view
from rest_framework.response import Response

from mainapp.models import Hotel, Review
from mainapp.serializers import HotelSerializer, ReviewSerializer


@api_view(['GET'])
def api_hotels(request):
    hotels = Hotel.objects.filter(is_active=True)
    serializer = HotelSerializer(hotels, many=True)
    return Response(serializer.data)

@api_view(['GET'])
def api_hotels_review(request, hotel_id):
    reviews = Review.objects.filter(hotel_id=hotel_id)
    serializer = ReviewSerializer(reviews, many=True)
    return Response(serializer.data)