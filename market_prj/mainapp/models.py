from django.db import models
from django.db.models import Avg
from userapp.models import CustomUser
from django.core.validators import MinValueValidator, MaxValueValidator
from django.core.exceptions import ValidationError
from django.db.models import Q


class ListOfCountries(models.Model):
    name = models.CharField(verbose_name='имя', max_length=64, unique=True)
    description = models.TextField(verbose_name='описание', blank=True)
    is_active = models.BooleanField(verbose_name='активна', default=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Страна'
        verbose_name_plural = 'Страны'
        ordering = ['name']


class Regions(models.Model):
    country = models.ForeignKey(ListOfCountries, on_delete=models.CASCADE, related_name='regions') # related_name='regions' задаёт имя обратной связи от связанной модели.
    name = models.CharField(max_length=64, verbose_name='имя')
    description = models.TextField(blank=True, verbose_name='описание')
    is_active = models.BooleanField(default=True, verbose_name='активна')

    def __str__(self):
        return self.name

    class Meta:
        unique_together = ('country', 'name') # в одной и той же стране не может быть два объекта с одним именем
        verbose_name = 'Регион'
        verbose_name_plural = 'Регионы'
        ordering = ['country', 'name'] # вариант сортировки, сперва по стране, потом по имени


class Hotel(models.Model):
    country = models.ForeignKey(ListOfCountries, on_delete=models.CASCADE, related_name='hotels')
    region = models.ForeignKey(Regions, on_delete=models.CASCADE, related_name='hotels')
    name = models.CharField('название', max_length=128)
    description = models.TextField('описание', blank=True)

    rating = models.DecimalField(max_digits=5, decimal_places=1, null=True, blank=True) # по рейтингу максимальное значение 5, после запятой одна цифра
    main_image = models.ImageField(upload_to='hotel_photos/', blank=True, null=True)
    is_active = models.BooleanField(default=True)

    created_at = models.DateTimeField(auto_now_add=True) # конда отель впервые добавили
    updated_at = models.DateTimeField(auto_now=True) # Знать когда последний раз меняли данные отеля
    deleted_at = models.DateTimeField(null=True, blank=True) # храним дату мягкого удаления отеля
    deleted = models.BooleanField(default=False) # помечать отель как удаленный, но не удалять из БД

    def average_rating(self):
        return self.reviews.filter(deleted=False).aggregate(avg=Avg('rating'))['avg']
# ф-ция подсчета рейтинга с фильтром на отзывы, которые не помечены как удаленные
# берет несколько строк из базы и возвращает одно итоговое значение.
# Avg - это агрегирующая ф-ция Django ORM, считает средне-арифметическое по указанному полю
    def __str__(self):
        return f'{self.name} ({self.country})'

    class Meta:
        verbose_name = 'Отель'
        verbose_name_plural = 'Отели'
        ordering = ['country', 'region', 'name']



class Room(models.Model):
    hotel = models.ForeignKey(Hotel, on_delete=models.CASCADE, related_name='rooms')

    room_type = models.CharField(max_length=128, verbose_name='тип номера')
    description = models.TextField(blank=True, verbose_name='описание номера')
    total_rooms = models.PositiveIntegerField(default=1)
    price_per_night = models.DecimalField(max_digits=8, decimal_places=2)


    image = models.ImageField(upload_to='room_img/', blank=True, null=True)

    # мягкое удаление + отметка времени
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    deleted_at = models.DateTimeField(null=True, blank=True) # вместо того чтобы удалять запись из БД, там записывают дату удаления, если поле пустое, объект активный, если есть дата, значит удален
    deleted = models.BooleanField(default=False) # если False, объект активный, если True объект помечен как удаленный


    def __str__(self):
        return f"{self.room_type} — {self.hotel.name}"

    class Meta:
        verbose_name = "Номер"
        verbose_name_plural = "Номера"
        ordering = ['hotel', 'room_type']
        unique_together = ('hotel', 'room_type')



class Booking(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='bookings') # много объектов к одному пользователю, многие к одному. related_name='bookings' для получения объектов bookings с которыми связан пользователь
    room = models.ForeignKey(Room, on_delete=models.PROTECT, related_name='bookings') # каждое бронирование относится к конкретной комнате, через related_name можно получить все бронирования этой комнаты
    check_in = models.DateField() # дата заезда без времени заезда DateField
    check_out = models.DateField() # дата выезда
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    deleted = models.BooleanField(default=False)
    deleted_at = models.DateTimeField(null=True, blank=True)

    in_order = models.BooleanField(default=False)  # ← ВАЖНО новый объект создается in_order=False, когда объект становится частью заказа in_order=True

    @property
    def nights(self):
        return (self.check_out - self.check_in).days # возвращает количество ночей

    @property # 'этот декоратор позволяет вычислять как будто это обычное поле self.nights (переменная), а не self.nights() (метод)
    def total_cost(self):
        return self.nights * self.room.price_per_night # умножает количество ночей на цену этой комнаты за ночь self.room.price_per_night

    def __str__(self):
        return f'Бронирование #{self.pk} — {self.room}'




    @staticmethod
    def is_room_available(room, check_in, check_out):
        booked = Booking.objects.filter(
            room=room,
            deleted=False,
            in_order = False
        ).filter(
            Q(check_in__lt=check_out) & Q(check_out__gt=check_in)
        ).count()
        return booked < room.total_rooms

    def clean(self):
        if self.check_out <= self.check_in:
            raise ValidationError('Дата выезда должна быть позже даты заезда')

        if not self.room:
            raise ValidationError({'room': 'Номер не выбран'})

        if not Booking.is_room_available(self.room, self.check_in, self.check_out):
            raise ValidationError('Номер уже забронирован на выбранные даты')

# def clean(self):
#     if self.check_in and self.check_out:
#         if self.check_out <= self.check_in:
#             raise ValidationError('Дата выезда должна быть позже даты заезда')
#
#         if not Booking.is_room_available(self.room, self.check_in, self.check_out):
#             raise ValidationError('Номер уже забронирован на выбранные даты')
#
#     if not self.room:
#         raise ValidationError({'room': 'Номер не выбран'})


class Review(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='reviews')
    hotel = models.ForeignKey(Hotel, on_delete=models.CASCADE, related_name='reviews')

    comment = models.TextField()
    rating = models.PositiveSmallIntegerField(validators=[MinValueValidator(1), MaxValueValidator(5)])

    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    deleted = models.BooleanField(default=False)

    class Meta:
        unique_together = ('user', 'hotel')


