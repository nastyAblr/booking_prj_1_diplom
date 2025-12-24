from django.db import models
from django.conf import settings
from mainapp.models import Booking


# заказ
class Order(models.Model):
    STATUS_CHOICES = [
        ('forming', 'Формируется'),
        ('processing', 'В обработке'),
        ('paid', 'Оплачен'),
        ('ready', 'Подтверждён'),
        ('cancelled', 'Отменён'),
    ]

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='orders')
    status = models.CharField(verbose_name='статус', max_length=20, choices=STATUS_CHOICES, default='forming')
    created = models.DateTimeField(auto_now_add=True, verbose_name='создан')
    updated = models.DateTimeField(auto_now=True, verbose_name='обновлён')
    is_active = models.BooleanField(default=True, verbose_name='активен')

    class Meta:
        verbose_name = 'заказ'
        verbose_name_plural = 'заказы'
        ordering = ('-created',)

    @property
    def total_nights(self):
        return sum(item.nights for item in self.items.all())

    @property
    def total_cost(self):
        return sum(item.cost for item in self.items.all())

    def cancel_order(self):
        for item in self.items.all():
            item.booking.in_order = False
            item.booking.save()

        self.status = 'cancelled'
        self.is_active = False
        self.save()


# Товарная позиция заказа

class OrderItem(models.Model):
    order = models.ForeignKey(Order, related_name='items', on_delete=models.CASCADE)
    booking = models.ForeignKey(Booking, verbose_name='бронирование',
                                on_delete=models.CASCADE)  # каждая товарная позиция взята из таблицы с предложениями (путевками)

    @property
    def nights(self):
        return (self.booking.check_out - self.booking.check_in).days

    @property
    def cost(self):
        return self.nights * self.booking.room.price_per_night

