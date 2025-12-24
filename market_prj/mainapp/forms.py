from mainapp.models import ListOfCountries, Regions, Hotel, Room
from django import forms
from .models import Review, Booking


class ListOfCountriesForm(forms.ModelForm):
    class Meta:
        model = ListOfCountries
        fields = ['name', 'description', 'is_active']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control'
            field.help_text = ''


class RegionForm(forms.ModelForm):
    class Meta:
        model = Regions
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control'
            field.help_text = ''


class HotelForm(forms.ModelForm):
    class Meta:
        model = Hotel
        fields = [
            'country', 'region', 'name', 'description',
            'rating', 'main_image', 'is_active'
        ]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Bootstrap классы
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control'
            field.help_text = ''

        # Фильтрация регионов по выбранной стране
        if 'country' in self.data:
            try:
                country_id = int(self.data.get('country'))
                self.fields['region'].queryset = Regions.objects.filter(country_id=country_id)
            except (ValueError, TypeError):
                pass
        elif self.instance.pk:
            self.fields['region'].queryset = Regions.objects.filter(
                country=self.instance.country
            )
        else:
            self.fields['region'].queryset = Regions.objects.none()


class RoomForm(forms.ModelForm):
    class Meta:
        model = Room
        fields = [
            'room_type', 'description',
            'price_per_night', 'total_rooms', 'image'
        ]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs['class'] = 'form-control'
            field.help_text = ''


class ReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = ['hotel', 'comment', 'rating']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs['class'] = 'form-control'
            field.help_text = ''



class BookingForm(forms.ModelForm):
    class Meta:
        model = Booking
        fields = ('room', 'check_in', 'check_out')
        widgets = {
            'room': forms.HiddenInput(),
            'check_in': forms.DateInput(
                attrs={'type': 'date', 'class': 'form-control'}
            ),
            'check_out': forms.DateInput(
                attrs={'type': 'date', 'class': 'form-control'}
            ),
        }

from datetime import date

today = date.today().isoformat()

widgets = {
    'check_in': forms.DateInput(attrs={
        'type': 'date',
        'min': today
    }),
    'check_out': forms.DateInput(attrs={
        'type': 'date',
        'min': today
    }),
}
