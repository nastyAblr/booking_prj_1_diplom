from django.contrib import admin
from .models import ListOfCountries, Regions, Hotel, Room
from django.db.models import Avg



#  Страны

@admin.register(ListOfCountries)
class ListOfCountriesAdmin(admin.ModelAdmin):
    list_display = ('name', 'is_active')
    list_editable = ('is_active',)
    search_fields = ('name',)
    ordering = ('name',)



#  Регионы

@admin.register(Regions)
class RegionsAdmin(admin.ModelAdmin):
    list_display = ('name', 'country', 'is_active')
    list_editable = ('is_active',)
    list_filter = ('country',)
    search_fields = ('name',)
    ordering = ('country', 'name')



#   INLINE для номеров в отеле Управление номерами

class RoomInline(admin.TabularInline):
    model = Room
    extra = 1               # количество пустых форм
    fields = ('room_type', 'price_per_night',  'deleted')
    readonly_fields = []
    show_change_link = True



#   Отели

@admin.register(Hotel)
class HotelAdmin(admin.ModelAdmin):
    list_display = ('name', 'country', 'average_rating', 'region', 'rating', 'is_active', 'deleted')
    list_editable = ('is_active',)
    list_filter = ('country', 'region', 'is_active', 'deleted')
    search_fields = ('name', 'country__name', 'region__name')
    ordering = ('country', 'region', 'name')
    inlines = [RoomInline]

    def average_rating(self, obj):
        avg = obj.reviews.filter(deleted=False).aggregate(avg=Avg('rating'))['avg']
        return round(avg, 2) if avg else '-'

    average_rating.short_description = 'Средний рейтинг'







