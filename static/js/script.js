// Main JavaScript for Ali's Halal Food Restaurant

document.addEventListener('DOMContentLoaded', function() {
    // Menu category filtering
    const categoryButtons = document.querySelectorAll('.category-btn');
    const menuItems = document.querySelectorAll('.menu-item');
    if (categoryButtons.length > 0) {
        categoryButtons.forEach(button => {
            button.addEventListener('click', () => {
                // Remove active class from all buttons
                categoryButtons.forEach(btn => btn.classList.remove('active'));
                
                // Add active class to clicked button
                button.classList.add('active');
                
                // Get category value
                const category = button.getAttribute('data-category');
                
                // Filter menu items
                menuItems.forEach(item => {
                    if (category === 'all' || item.getAttribute('data-category') === category) {
                        item.style.display = 'block';
                    } else {
                        item.style.display = 'none';
                    }
                });
            });
        });
    }
  // Booking form date validation
  const dateInput = document.getElementById('date');
  if (dateInput) {
      // Set min date to today
      const today = new Date();
      const dd = String(today.getDate()).padStart(2, '0');
      const mm = String(today.getMonth() + 1).padStart(2, '0');
      const yyyy = today.getFullYear();
      const todayString = yyyy + '-' + mm + '-' + dd;
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
   // Simple form validation
   const forms = document.querySelectorAll('form');
   forms.forEach(form => {
       form.addEventListener('submit', function(event) {
           const requiredFields = form.querySelectorAll('[required]');
           let isValid = true;
           
           requiredFields.forEach(field => {
               if (!field.value.trim()) {
                   isValid = false;
                   field.classList.add('error');
               } else {
                   field.classList.remove('error');
               }
           });
           
           if (!isValid) {
               event.preventDefault();
               alert('Please fill in all required fields.');
           }
       });
   });
    // Testimonial slider auto-scroll
    const testimonialSlider = document.querySelector('.testimonials-slider');
    if (testimonialSlider && testimonialSlider.children.length > 1) {
        let currentIndex = 0;
        const testimonials = testimonialSlider.children;
        
        setInterval(() => {
            currentIndex = (currentIndex + 1) % testimonials.length;
            testimonialSlider.scrollTo({
                left: testimonials[currentIndex].offsetLeft,
                behavior: 'smooth'
            });
        }, 5000);
    }
});
