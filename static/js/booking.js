// Additional JavaScript for booking functionality

document.addEventListener('DOMContentLoaded', function() {
    // Elements for booking form
    const dateInput = document.getElementById('date');
    const timeInput = document.getElementById('time');
    const guestsInput = document.getElementById('guests');
    const bookingForm = document.querySelector('form[action*="booking"]');

    if (bookingForm) {
        // Set min date to today
        const today = new Date();
        const dd = String(today.getDate()).padStart(2, '0');
        const mm = String(today.getMonth() + 1).padStart(2, '0');
        const yyyy = today.getFullYear();
        const todayString = yyyy + '-' + mm + '-' + dd;
        if (dateInput) {
            dateInput.setAttribute('min', todayString);
            
            // Set max date to 30 days from today
            const maxDate = new Date();
            maxDate.setDate(maxDate.getDate() + 30);
            const maxDd = String(maxDate.getDate()).padStart(2, '0');
            const maxMm = String(maxDate.getMonth() + 1).padStart(2, '0');
            const maxYyyy = maxDate.getFullYear();
            const maxDateString = maxYyyy + '-' + maxMm + '-' + maxDd;
            dateInput.setAttribute('max', maxDateString);
        }
         // Check availability when inputs change
         if (dateInput && timeInput && guestsInput) {
            [dateInput, timeInput, guestsInput].forEach(input => {
                input.addEventListener('change', checkAvailability);
            });
        }
         // Form submission validation
         bookingForm.addEventListener('submit', function(event) {
            if (!validateBookingForm()) {
                event.preventDefault();
            }
        });
    }

     // Function to check table availability
    function checkAvailability() {
        const date = dateInput.value;
        const time = timeInput.value;
        const guests = guestsInput.value;

         // Only check if all values are provided
        if (!date || !time || !guests) {
            return;
        }
         // Show loading indicator
         const availabilityMessage = document.getElementById('availability-message') || 
         createAvailabilityMessage();
         availabilityMessage.textContent = 'Checking availability...';
         availabilityMessage.className = 'availability-message checking';

          // Make API request to check availability
        fetch('/api/check-availability', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ date, time, guests }),
        })

        .then(response => response.json())
        .then(data => {
            if (data.available) {
                availabilityMessage.textContent = `Available! ${data.tables} table(s) available for your party.`;
                availabilityMessage.className = 'availability-message available';
            } else {
                availabilityMessage.textContent = 'Sorry, no tables available at this time. Please try another date or time.';
                availabilityMessage.className = 'availability-message unavailable';
            }
        })
        .catch(error => {
            console.error('Error checking availability:', error);
            availabilityMessage.textContent = 'Error checking availability. Please try again.';
            availabilityMessage.className = 'availability-message error';
        });
    }
    
    // Create availability message element
    function createAvailabilityMessage() {
        const messageDiv = document.createElement('div');
        messageDiv.id = 'availability-message';
        messageDiv.className = 'availability-message';
        
        // Find where to insert the message
        const timeGroup = timeInput.closest('.form-group');
        timeGroup.parentNode.insertBefore(messageDiv, timeGroup.nextSibling);
        
        return messageDiv;
    }
    
     // Validate booking form before submission
     function validateBookingForm() {
        const name = document.getElementById('name').value;
        const email = document.getElementById('email').value;
        const phone = document.getElementById('phone').value;
        const date = dateInput.value;
        const time = timeInput.value;
        const guests = guestsInput.value;
         // Basic validation
         if (!name || !email || !phone || !date || !time || !guests) {
            alert('Please fill in all required fields.');
            return false;
        }
        
        // Email validation
        const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
        if (!emailRegex.test(email)) {
            alert('Please enter a valid email address.');
            return false;
        }
        
        // Phone validation
        const phoneRegex = /^\d{10,15}$/;
        if (!phoneRegex.test(phone.replace(/[^0-9]/g, ''))) {
            alert('Please enter a valid phone number.');
            return false;
        }

        // Date validation
        const selectedDate = new Date(date);
        const today = new Date();
        today.setHours(0, 0, 0, 0);
        
        if (selectedDate < today) {
            alert('Please select a future date.');
            return false;
        }
        
        const maxDate = new Date();
        maxDate.setDate(maxDate.getDate() + 30);
        maxDate.setHours(0, 0, 0, 0);
        
        if (selectedDate > maxDate) {
            alert('Bookings can only be made up to 30 days in advance.');
            return false;
        }
        // Check availability message
        const availabilityMessage = document.getElementById('availability-message');
        if (availabilityMessage && availabilityMessage.className.includes('unavailable')) {
            alert('Sorry, no tables are available for the selected date and time. Please choose another time or date.');
            return false;
        }
        
        return true;
    }
});


