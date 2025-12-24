from rest_framework import serializers
from mainapp.models import ListOfCountries, Regions, Hotel, Review


class CountrySerializer(serializers.ModelSerializer):
    class Meta:
        model = ListOfCountries
        fields = ['id', 'name']

class RegionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Regions
        fields = ['id', 'name', 'country']

class HotelSerializer(serializers.ModelSerializer):
    class Meta:
        model = Hotel
        fields = ['id', 'name', 'region']

class ReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Review
        fields = ['id', 'user', 'rating', 'comment', 'created']