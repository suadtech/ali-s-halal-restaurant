from django import forms
from .models import Booking
from datetime import datetime, time, timedelta

class BookingForm(forms.ModelForm):
    class Meta:
        model = Booking
        fields = ['booking_date', 'booking_time', 'guests', 'special_requests']
        widgets = {
            'booking_date': forms.DateInput(attrs={'type': 'date'}),
            'booking_time': forms.Select(choices=[
                (time(hour=10), '10:00 AM'),
                (time(hour=11), '11:00 AM'),
                (time(hour=12), '12:00 PM'),
                (time(hour=13), '1:00 PM'),
                (time(hour=14), '2:00 PM'),
                (time(hour=15), '3:00 PM'),
                (time(hour=16), '4:00 PM'),
                (time(hour=17), '5:00 PM'),
                (time(hour=18), '6:00 PM'),
                (time(hour=19), '7:00 PM'),
                (time(hour=20), '8:00 PM'),
                (time(hour=21), '9:00 PM'),
            ]),
        }
    def clean_booking_date(self):
        date = self.cleaned_data.get('booking_date')
        today = datetime.now().date()
        
        if date < today:
            raise forms.ValidationError("Booking date cannot be in the past.")
        
        max_date = today + timedelta(days=30)
        if date > max_date:
            raise forms.ValidationError("Bookings can only be made up to 30 days in advance.")
            
        return date
        def clean_guests(self):
        guests = self.cleaned_data.get('guests')
        
        if guests < 1:
            raise forms.ValidationError("Number of guests must be at least 1.")
        if guests > 10:
            raise forms.ValidationError("For parties larger than 10, please call us directly.")
            
        return guests