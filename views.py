from flask import render_template, request, redirect, url_for, flash, jsonify
from flask_login import login_user, login_required, logout_user, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime, timedelta

from models import db, User, Table, Booking, MenuCategory, MenuItem, Contact

# Home page
def home():
    return render_template('index.html')

# Menu page
def menu():
    categories = MenuCategory.query.all()
    menu_items = MenuItem.query.filter_by(is_available=True).all()
    return render_template('menu.html', categories=categories, menu_items=menu_items)

  # Booking page and booking processing
def booking():
    if request.method == 'POST':
        # Get form data
        name = request.form.get('name')
        email = request.form.get('email')
        phone = request.form.get('phone')
        guests = int(request.form.get('guests'))
        date_str = request.form.get('date')
        time_str = request.form.get('time')
        special_requests = request.form.get('special_requests')

   # Convert date and time strings to Python objects
        booking_date = datetime.strptime(date_str, '%Y-%m-%d').date()
        booking_time = datetime.strptime(time_str, '%H:%M').time()
   # Find available tables for the requested date, time, and party size
        available_tables = find_available_tables(booking_date, booking_time, guests)
        
        if not available_tables:
            flash('Sorry, no tables are available for the selected date and time. Please try another time or date.', 'danger')
            return redirect(url_for('booking'))   

   # Create a new user if not logged in
        if not current_user.is_authenticated:
            # Check if user with this email already exists
            user = User.query.filter_by(email=email).first()
            if not user:
                # Create a new user with a temporary password
                temp_password = generate_password_hash('temporary')
                user = User(name=name, email=email, password=temp_password)
                db.session.add(user)
                db.session.commit()
            user_id = user.id
        else:
            user_id = current_user.id

  # Create a new booking with the first available table
        new_booking = Booking(
            user_id=user_id,
            table_id=available_tables[0].id,
            booking_date=booking_date,
            booking_time=booking_time,
            guests=guests,
            special_requests=special_requests
        )
        
        db.session.add(new_booking)
        db.session.commit()
        
        flash('Your booking has been confirmed!', 'success')
        return redirect(url_for('booking_confirmation', booking_id=new_booking.id))
    
    return render_template('booking.html')

 # Booking confirmation page
def booking_confirmation(booking_id):
    booking = Booking.query.get_or_404(booking_id)
    return render_template('booking_confirmation.html', booking=booking)

 # Contact page
def contact():
    if request.method == 'POST':
        name = request.form.get('name')
        email = request.form.get('email')
        subject = request.form.get('subject')
        message = request.form.get('message')
        
        new_contact = Contact(
            name=name,
            email=email,
            subject=subject,
            message=message
        )
        
        db.session.add(new_contact)
        db.session.commit()
        
        flash('Your message has been sent! We will get back to you soon.', 'success')
        return redirect(url_for('contact'))
    
    return render_template('contact.html')
  # Admin dashboard
@login_required
def admin():
    if not current_user.is_admin:
        flash('You do not have permission to access the admin area.', 'danger')
        return redirect(url_for('home'))
    
    bookings = Booking.query.order_by(Booking.booking_date.desc()).all()
    tables = Table.query.all()
    menu_items = MenuItem.query.all()
    contacts = Contact.query.order_by(Contact.created_at.desc()).all()
    
    return render_template('admin.html', 
                          bookings=bookings, 
                          tables=tables, 
                          menu_items=menu_items, 
                          contacts=contacts)
  # User registration
def register():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    
    if request.method == 'POST':
        name = request.form.get('name')
        email = request.form.get('email')
        password = request.form.get('password')
        confirm_password = request.form.get('confirm_password')

    # Validate input
        if not name or not email or not password or not confirm_password:
            flash('All fields are required.', 'danger')
            return render_template('register.html')
        
        if password != confirm_password:
            flash('Passwords do not match.', 'danger')
            return render_template('register.html')    
                             
# Check if email already exists
        existing_user = User.query.filter_by(email=email).first()
        if existing_user:
            flash('Email already registered. Please use a different email or login.', 'danger')
            return render_template('register.html')
        
 # Create new user
        hashed_password = generate_password_hash(password)
        new_user = User(name=name, email=email, password=hashed_password)
        db.session.add(new_user)
        db.session.commit()
        
        flash('Registration successful! You can now login.', 'success')
        return redirect(url_for('login'))
    
    return render_template('register.html')

  
# User login
def login():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        
        user = User.query.filter_by(email=email).first()
        
        if user and check_password_hash(user.password, password):
            login_user(user)
            next_page = request.args.get('next')
            return redirect(next_page or url_for('home'))
        else:
            flash('Login failed. Please check your email and password.', 'danger')
    
    return render_template('login.html')

 # User logout
@login_required
def logout():
    logout_user()
    return redirect(url_for('home'))

  # User profile
@login_required
def profile():
    # Get user's bookings
    bookings = Booking.query.filter_by(user_id=current_user.id).order_by(Booking.booking_date.desc()).all()
    return render_template('profile.html', bookings=bookings)

  # Edit user profile
@login_required
def edit_profile():
    if request.method == 'POST':
        name = request.form.get('name')
        email = request.form.get('email')
        current_password = request.form.get('current_password')
        new_password = request.form.get('new_password')
        confirm_password = request.form.get('confirm_password')
        
       # Validate current password
        if not check_password_hash(current_user.password, current_password):
            flash('Current password is incorrect.', 'danger')
            return redirect(url_for('edit_profile'))

         # Check if email already exists (if changed)
        if email != current_user.email:
            existing_user = User.query.filter_by(email=email).first()
            if existing_user:
                flash('Email already in use by another account.', 'danger')
                return redirect(url_for('edit_profile'))
        
        # Update user information
        current_user.name = name
        current_user.email = email
        
        # Update password if provided
        if new_password:
            if new_password != confirm_password:
                flash('New passwords do not match.', 'danger')
                return redirect(url_for('edit_profile'))
            
            current_user.password = generate_password_hash(new_password)
        
        db.session.commit()
        flash('Profile updated successfully!', 'success')
        return redirect(url_for('profile'))
    
    return render_template('edit_profile.html')

# Cancel booking
@login_required
def cancel_booking(booking_id):
    booking = Booking.query.get_or_404(booking_id)
    
    # Check if user is authorized to cancel this booking
    if booking.user_id != current_user.id and not current_user.is_admin:
        flash('You are not authorized to cancel this booking.', 'danger')
        return redirect(url_for('home'))
    
    booking.status = 'cancelled'
    db.session.commit()
    
    flash('Your booking has been cancelled.', 'success')
    return redirect(url_for('home'))

# Manage bookings (admin)
@login_required
def manage_bookings():
    if not current_user.is_admin:
        flash('You do not have permission to access this page.', 'danger')
        return redirect(url_for('home'))
    
    if request.method == 'POST':
        booking_id = request.form.get('booking_id')
        action = request.form.get('action')
        
        booking = Booking.query.get_or_404(booking_id)
        
        if action == 'cancel':
            booking.status = 'cancelled'
            flash(f'Booking #{booking_id} has been cancelled.', 'success')
        elif action == 'complete':
            booking.status = 'completed'
            flash(f'Booking #{booking_id} has been marked as completed.', 'success')
        
        db.session.commit()

        # Get all bookings for display
    bookings = Booking.query.order_by(Booking.booking_date.desc()).all()
    return render_template('admin_bookings.html', bookings=bookings)

# Manage tables (admin)
@login_required
def manage_tables():
    if not current_user.is_admin:
        flash('You do not have permission to access this page.', 'danger')
        return redirect(url_for('home'))
    
    if request.method == 'POST':
        action = request.form.get('action')
        
        if action == 'add':
            table_number = request.form.get('table_number')
            capacity = request.form.get('capacity')
            
            # Check if table number already exists
            existing_table = Table.query.filter_by(table_number=table_number).first()
            if existing_table:
                flash(f'Table #{table_number} already exists.', 'danger')
            else:
                new_table = Table(table_number=table_number, capacity=capacity)
                db.session.add(new_table)
                db.session.commit()
                flash(f'Table #{table_number} has been added.', 'success')
        elif action == 'toggle':
            table_id = request.form.get('table_id')
            table = Table.query.get_or_404(table_id)
            table.is_active = not table.is_active
            db.session.commit()
            status = 'activated' if table.is_active else 'deactivated'
            flash(f'Table #{table.table_number} has been {status}.', 'success')

            # Get all tables for display
    tables = Table.query.order_by(Table.table_number).all()
    return render_template('admin_tables.html', tables=tables)
# Manage menu (admin)
@login_required
def manage_menu():
    if not current_user.is_admin:
        flash('You do not have permission to access this page.', 'danger')
        return redirect(url_for('home'))
    
    if request.method == 'POST':
        action = request.form.get('action')
        
        if action == 'add':
            name = request.form.get('name')
            category_id = request.form.get('category_id')
            price = float(request.form.get('price'))
            description = request.form.get('description')
            image = request.form.get('image')

            new_item = MenuItem(
                name=name,
                category_id=category_id,
                price=price,
                description=description,
                image=image,
                is_available=True
            )
            db.session.add(new_item)
            db.session.commit()
            flash(f'Menu item "{name}" has been added.', 'success')
        elif action == 'edit':
            item_id = request.form.get('item_id')
            item = MenuItem.query.get_or_404(item_id)
            
            item.name = request.form.get('name')
            item.category_id = request.form.get('category_id')
            item.price = float(request.form.get('price'))
            item.description = request.form.get('description')
            item.image = request.form.get('image')
            
            db.session.commit()
            flash(f'Menu item "{item.name}" has been updated.', 'success')
        elif action == 'toggle':
            item_id = request.form.get('item_id')
            item = MenuItem.query.get_or_404(item_id)
            item.is_available = not item.is_available
            db.session.commit()
            status = 'available' if item.is_available else 'unavailable'
            flash(f'Menu item "{item.name}" is now {status}.', 'success')
        
        elif action == 'add_category':
            category_name = request.form.get('category_name')
            # Check if category already exists
            existing_category = MenuCategory.query.filter_by(name=category_name).first()
            if existing_category:
                flash(f'Category "{category_name}" already exists.', 'danger')
            else:
                new_category = MenuCategory(name=category_name)
                db.session.add(new_category)
                db.session.commit()
                flash(f'Category "{category_name}" has been added.', 'success')
        
        elif action == 'delete_category':
            category_id = request.form.get('category_id')
            category = MenuCategory.query.get_or_404(category_id)
            # Check if category has menu items
            if MenuItem.query.filter_by(category_id=category_id).first():
                flash(f'Cannot delete category "{category.name}" because it contains menu items.', 'danger')
            else:
                db.session.delete(category)
                db.session.commit()
                flash(f'Category "{category.name}" has been deleted.', 'success')
    # Get all menu items and categories for display
    menu_items = MenuItem.query.all()
    categories = MenuCategory.query.all()
    return render_template('admin_menu.html', menu_items=menu_items, categories=categories)

# Check availability API
def check_availability():
    data = request.get_json()
    
    date_str = data.get('date')
    time_str = data.get('time')
    guests = int(data.get('guests'))
    
    booking_date = datetime.strptime(date_str, '%Y-%m-%d').date()
    booking_time = datetime.strptime(time_str, '%H:%M').time()
    
    available_tables = find_available_tables(booking_date, booking_time, guests)
    
    return jsonify({
        'available': len(available_tables) > 0,
        'tables': len(available_tables)
    })
# Helper function to find available tables
def find_available_tables(booking_date, booking_time, guests):
    # Find tables that can accommodate the party size
    suitable_tables = Table.query.filter(Table.capacity >= guests, Table.is_active == True).order_by(Table.capacity).all()
    
    if not suitable_tables:
        return []
    # Check which tables are already booked at the requested time
    # Assuming bookings are 2 hours long
    booking_datetime = datetime.combine(booking_date, booking_time)
    booking_end = (datetime.combine(booking_date, booking_time) + timedelta(hours=2)).time()
    
    available_tables = []
    
    for table in suitable_tables:
      # Check if table is already booked at this time
        existing_bookings = Booking.query.filter(
            Booking.table_id == table.id,
            Booking.booking_date == booking_date,
            Booking.status == 'confirmed'
        ).all()
        
        is_available = True
        
        for existing in existing_bookings:
            existing_start = existing.booking_time
            existing_end = (datetime.combine(booking_date, existing_start) + timedelta(hours=2)).time()

         # Check if there's an overlap
            if (booking_time >= existing_start and booking_time < existing_end) or \
               (booking_end > existing_start and booking_end <= existing_end) or \
               (booking_time <= existing_start and booking_end >= existing_end):
                is_available = False
                break
           if is_available:
            available_tables.append(table)
    
    return available_tables
        