
from django.shortcuts import get_object_or_404, redirect, render
from orderapp.models import Order, OrderItem
from mainapp.models import Booking
from django.contrib.auth.decorators import login_required


# Список заказов

@login_required
def order_list(request):
    orders = Order.objects.filter(user=request.user).order_by('-created')
    return render(request, 'orderapp/order_list.html', {'orders': orders})

# Детали заказов

@login_required
def order_detail(request, pk):
    order = get_object_or_404(Order, pk=pk, user=request.user)
    return render(request, 'orderapp/order_detail.html', {'order': order})

# Создание заказа из бронирований(создается из ранее созданных бронирований)


@login_required
def order_create(request):
    # получаем бронирование текущего пользователя, которого еще нет в заказе
    bookings = Booking.objects.filter(user=request.user, in_order=False, deleted=False)

    if not bookings.exists():
        # если неи активных бронирований - выводим
        return redirect('mainapp:booking_list')

    if request.method == 'POST':

        # создаем новый заказ
        order = Order.objects.create(user=request.user, status='forming')

        # создаем OrderItem для каждого бронирования
        for booking in bookings:
            OrderItem.objects.create(
                order=order,
                booking=booking,)
        # отмечаем бронирование как включенное в заказ
            booking.in_order = True
            booking.save()

        # Перенаправляем на страницу
        return redirect('orderapp:order_confirm', pk=order.pk)

    return render(request, 'orderapp/order_create.html', {'bookings': bookings})


# Подтверждение заказа (тот самый /confirm)

@login_required
def order_confirm(request, pk):
    order = get_object_or_404(Order, pk=pk, user=request.user)
# ЗАЩИТА ОТ ПОВТОРНОГО ПОДТВЕРЖДЕНИЯ
    if order.status != 'forming':
        return redirect('orderapp:order_list')

    if request.method == 'POST':
        order.status = 'processing'
        order.save()
        return redirect('orderapp:order_list')

    return render(request, 'orderapp/order_confirmed.html', {'order': order})

# Отмена заказа

@login_required
def order_cancel(request, pk):
    order = get_object_or_404(Order, pk=pk, user=request.user)

# ЗАЩИТА ОТ ДВОЙНОГО УДАЛЕНИЯ
    if order.status not in ('forming', 'processing'):
        return redirect('orderapp:order_list')

    order.cancel_order()
    return redirect('orderapp:order_list')


@login_required
def order_success(request):
    return render(request, 'orderapp/order_list.html')






