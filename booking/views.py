from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from datetime import datetime, timedelta
from .models import Booking, Table
from .forms import BookingForm 
# Create your views here.
def booking_form(request):
    if request.method == 'POST':
        form = BookingForm(request.POST)
        if form.is_valid():
            booking = form.save(commit=False)

            if request.user.is_authenticated:
                booking.user = request.user

                # Find available tables
            available_tables = find_available_tables(
                booking.booking_date,
                booking.booking_time,
                booking.guests
            )
            if available_tables:
                booking.table = available_tables[0]
                booking.save()
                messages.success(request, 'Your booking has been confirmed!')
                return redirect('booking:booking_confirmation', booking_id=booking.id)
            else:
                messages.error(request, 'Sorry, no tables are available for the selected date and time.')
    else:
        form = BookingForm()

    return render(request, 'booking/booking_form.html', {'form': form})
def booking_confirmation(request, booking_id):
    booking = get_object_or_404(Booking, id=booking_id)
    return render(request, 'booking/booking_confirmation.html', {'booking': booking})

@login_required
def cancel_booking(request, booking_id):
    booking = get_object_or_404(Booking, id=booking_id) 

    if booking.user == request.user or request.user.is_staff:
        booking.status = 'cancelled'
        booking.save()
        messages.success(request, 'Your booking has been cancelled.')
    else:
        messages.error(request, 'You are not authorized to cancel this booking.')
    
    return redirect('profile')
def find_available_tables(booking_date, booking_time, guests):
    # Logic to find available tables
    suitable_tables = Table.objects.filter(capacity__gte=guests, is_active=True).order_by('capacity')
    
    if not suitable_tables:
        return []
    
    booking_datetime = datetime.combine(booking_date, booking_time)
    booking_end_datetime = booking_datetime + timedelta(hours=2)
    
    available_tables = []
    
    for table in suitable_tables:
        existing_bookings = Booking.objects.filter(
            table=table,
            booking_date=booking_date,
            status='confirmed'
        )

        is_available = True
        
        for existing in existing_bookings:
            existing_start = datetime.combine(booking_date, existing.booking_time)
            existing_end = existing_start + timedelta(hours=2)

            if (booking_datetime >= existing_start and booking_datetime < existing_end) or \
               (booking_end_datetime > existing_start and booking_end_datetime <= existing_end) or \
               (booking_datetime <= existing_start and booking_end_datetime >= existing_end):
                is_available = False
                break
        
        if is_available:
            available_tables.append(table)
    
    return available_tables
            

             