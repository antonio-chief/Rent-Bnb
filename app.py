from flask import Flask, render_template, request, redirect, url_for, session, flash, jsonify
from werkzeug.security import generate_password_hash, check_password_hash
from werkzeug.utils import secure_filename
from datetime import datetime, timedelta
import sqlite3
import os
from functools import wraps

app = Flask(__name__)
app.secret_key = 'your-secret-key-here-change-in-production'

DATABASE = 'rentbnb.db'
UPLOAD_FOLDER = 'static/uploads'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif', 'webp'}

# Create uploads folder if it doesn't exist
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB max file size

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

# Database helper functions
def get_db():
    db = sqlite3.connect(DATABASE)
    db.row_factory = sqlite3.Row
    return db

def init_db():
    """Initialize the database with tables"""
    with app.app_context():
        db = get_db()
        with app.open_resource('schema.sql', mode='r') as f:
            db.cursor().executescript(f.read())
        db.commit()

# Login required decorator
def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session:
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return decorated_function

# Admin required decorator
def admin_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session or session.get('role') != 'admin':
            flash('Access denied. Admin privileges required.')
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return decorated_function

# Routes
@app.route('/')
def index():
    if 'user_id' in session:
        if session.get('role') == 'admin':
            return redirect(url_for('admin_dashboard'))
        else:
            return redirect(url_for('client_dashboard'))
    return redirect(url_for('login'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = (request.form.get('email') or '').strip().lower()
        password = request.form.get('password')
        
        db = get_db()
        user = db.execute('SELECT * FROM users WHERE email = ?', (email,)).fetchone()
        
        if user and check_password_hash(user['password'], password):
            session['user_id'] = user['id']
            session['name'] = user['name']
            session['role'] = user['role']
            
            if user['role'] == 'admin':
                return redirect(url_for('admin_dashboard'))
            else:
                return redirect(url_for('client_dashboard'))
        else:
            flash('Invalid email or password')
    
    return render_template('login.html')

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        name = request.form.get('name')
        email = (request.form.get('email') or '').strip().lower()
        password = request.form.get('password')
        phone = request.form.get('phone', '')
        role = request.form.get('role', 'client')
        allowed_roles = {'client', 'admin'}
        if role not in allowed_roles:
            role = 'client'
        
        db = get_db()
        
        # Check if user already exists
        existing_user = db.execute('SELECT id FROM users WHERE email = ?', (email,)).fetchone()
        if existing_user:
            flash('Email already registered')
            return redirect(url_for('signup'))
        
        # Create new user
        hashed_password = generate_password_hash(password)
        db.execute(
            'INSERT INTO users (name, email, password, phone, role) VALUES (?, ?, ?, ?, ?)',
            (name, email, hashed_password, phone, role)
        )
        db.commit()
        
        flash('Registration successful! Please login.')
        return redirect(url_for('login'))
    
    return render_template('signup.html')

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('login'))

# Admin routes
@app.route('/admin/dashboard')
@admin_required
def admin_dashboard():
    db = get_db()
    
    # Get statistics
    total_bookings = db.execute('SELECT COUNT(*) as count FROM bookings').fetchone()['count']
    total_sales = db.execute('SELECT SUM(total_price) as total FROM bookings WHERE status != "cancelled"').fetchone()['total'] or 0
    check_ins = db.execute('SELECT COUNT(*) as count FROM bookings WHERE status = "checked_in"').fetchone()['count']
    
    # Get today's arrivals
    today = datetime.now().date()
    todays_arrivals = db.execute('''
        SELECT b.*, c.name as cabin_name, u.name as guest_name, u.email as guest_email
        FROM bookings b
        JOIN cabins c ON b.cabin_id = c.id
        JOIN users u ON b.user_id = u.id
        WHERE DATE(b.check_in) = ? AND b.status = "unconfirmed"
        ORDER BY b.check_in
    ''', (today,)).fetchall()
    
    # Get recent bookings
    recent_bookings = db.execute('''
        SELECT b.*, c.name as cabin_name, u.name as guest_name
        FROM bookings b
        JOIN cabins c ON b.cabin_id = c.id
        JOIN users u ON b.user_id = u.id
        ORDER BY b.created_at DESC
        LIMIT 10
    ''').fetchall()
    
    # Calculate occupancy rate (simplified)
    total_cabins = db.execute('SELECT COUNT(*) as count FROM cabins').fetchone()['count']
    occupied_cabins = db.execute('''
        SELECT COUNT(DISTINCT cabin_id) as count 
        FROM bookings 
        WHERE status = "checked_in" OR status = "unconfirmed"
    ''').fetchone()['count']
    occupancy_rate = (occupied_cabins / total_cabins * 100) if total_cabins > 0 else 0
    
    return render_template('admin_dashboard.html',
                         total_bookings=total_bookings,
                         total_sales=total_sales,
                         check_ins=check_ins,
                         occupancy_rate=occupancy_rate,
                         todays_arrivals=todays_arrivals,
                         recent_bookings=recent_bookings)

@app.route('/admin/bookings')
@admin_required
def admin_bookings():
    db = get_db()
    
    status_filter = request.args.get('status', 'all')
    
    query = '''
        SELECT b.*, c.name as cabin_name, c.cabin_number, 
               u.name as guest_name, u.email as guest_email
        FROM bookings b
        JOIN cabins c ON b.cabin_id = c.id
        JOIN users u ON b.user_id = u.id
    '''
    
    if status_filter != 'all':
        query += ' WHERE b.status = ?'
        bookings = db.execute(query + ' ORDER BY b.created_at DESC', (status_filter,)).fetchall()
    else:
        bookings = db.execute(query + ' ORDER BY b.created_at DESC').fetchall()
    
    return render_template('admin_bookings.html', bookings=bookings, status_filter=status_filter)

@app.route('/admin/booking/<int:booking_id>')
@admin_required
def admin_booking_detail(booking_id):
    db = get_db()
    
    booking = db.execute('''
        SELECT b.*, c.name as cabin_name, c.cabin_number, c.price_per_night,
               u.name as guest_name, u.email as guest_email, u.phone as guest_phone,
               u.national_id
        FROM bookings b
        JOIN cabins c ON b.cabin_id = c.id
        JOIN users u ON b.user_id = u.id
        WHERE b.id = ?
    ''', (booking_id,)).fetchone()
    
    if not booking:
        flash('Booking not found')
        return redirect(url_for('admin_bookings'))
    
    return render_template('admin_booking_detail.html', booking=booking)

@app.route('/admin/booking/<int:booking_id>/check-in', methods=['POST'])
@admin_required
def check_in_booking(booking_id):
    db = get_db()
    db.execute('UPDATE bookings SET status = "checked_in" WHERE id = ?', (booking_id,))
    db.commit()
    flash('Guest checked in successfully')
    return redirect(url_for('admin_booking_detail', booking_id=booking_id))

@app.route('/admin/booking/<int:booking_id>/check-out', methods=['POST'])
@admin_required
def check_out_booking(booking_id):
    db = get_db()
    db.execute('UPDATE bookings SET status = "checked_out" WHERE id = ?', (booking_id,))
    db.commit()
    flash('Guest checked out successfully')
    return redirect(url_for('admin_booking_detail', booking_id=booking_id))

@app.route('/admin/booking/<int:booking_id>/delete', methods=['POST'])
@admin_required
def delete_booking(booking_id):
    db = get_db()
    db.execute('DELETE FROM bookings WHERE id = ?', (booking_id,))
    db.commit()
    flash('Booking deleted successfully')
    return redirect(url_for('admin_bookings'))

@app.route('/admin/cabins')
@admin_required
def admin_cabins():
    db = get_db()
    cabins = db.execute('SELECT * FROM cabins ORDER BY cabin_number').fetchall()
    return render_template('admin_cabins.html', cabins=cabins)

@app.route('/admin/cabin/add', methods=['GET', 'POST'])
@admin_required
def add_cabin():
    if request.method == 'POST':
        name = request.form.get('name')
        cabin_number = request.form.get('cabin_number')
        capacity = request.form.get('capacity')
        price_per_night = request.form.get('price_per_night')
        description = request.form.get('description', '')
        amenities = request.form.get('amenities', '')
        image_url = request.form.get('image_url', '')
        
        # Handle file upload
        if 'image_file' in request.files:
            file = request.files['image_file']
            if file and file.filename and allowed_file(file.filename):
                filename = secure_filename(f"cabin_{cabin_number}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.{file.filename.rsplit('.', 1)[1].lower()}")
                file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
                image_url = f'/static/uploads/{filename}'
        
        db = get_db()
        db.execute('''
            INSERT INTO cabins (name, cabin_number, capacity, price_per_night, description, amenities, image_url)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        ''', (name, cabin_number, capacity, price_per_night, description, amenities, image_url))
        db.commit()
        
        flash('Cabin added successfully')
        return redirect(url_for('admin_cabins'))
    
    return render_template('admin_add_cabin.html')

@app.route('/admin/cabin/<int:cabin_id>/edit', methods=['GET', 'POST'])
@admin_required
def edit_cabin(cabin_id):
    db = get_db()
    
    if request.method == 'POST':
        name = request.form.get('name')
        cabin_number = request.form.get('cabin_number')
        capacity = request.form.get('capacity')
        price_per_night = request.form.get('price_per_night')
        description = request.form.get('description', '')
        amenities = request.form.get('amenities', '')
        image_url = request.form.get('image_url', '')
        
        # Handle file upload
        if 'image_file' in request.files:
            file = request.files['image_file']
            if file and file.filename and allowed_file(file.filename):
                filename = secure_filename(f"cabin_{cabin_number}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.{file.filename.rsplit('.', 1)[1].lower()}")
                file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
                image_url = f'/static/uploads/{filename}'
        
        db.execute('''
            UPDATE cabins 
            SET name = ?, cabin_number = ?, capacity = ?, price_per_night = ?, 
                description = ?, amenities = ?, image_url = ?
            WHERE id = ?
        ''', (name, cabin_number, capacity, price_per_night, description, amenities, image_url, cabin_id))
        db.commit()
        
        flash('Cabin updated successfully')
        return redirect(url_for('admin_cabins'))
    
    cabin = db.execute('SELECT * FROM cabins WHERE id = ?', (cabin_id,)).fetchone()
    return render_template('admin_edit_cabin.html', cabin=cabin)

@app.route('/admin/cabin/<int:cabin_id>/delete', methods=['POST'])
@admin_required
def delete_cabin(cabin_id):
    db = get_db()
    db.execute('DELETE FROM cabins WHERE id = ?', (cabin_id,))
    db.commit()
    flash('Cabin deleted successfully')
    return redirect(url_for('admin_cabins'))

@app.route('/admin/users')
@admin_required
def admin_users():
    db = get_db()
    users = db.execute('SELECT * FROM users ORDER BY created_at DESC').fetchall()
    return render_template('admin_users.html', users=users)

# Client routes
@app.route('/client/dashboard')
@login_required
def client_dashboard():
    db = get_db()
    
    # Get available cabins
    cabins = db.execute('SELECT * FROM cabins ORDER BY price_per_night').fetchall()
    
    # Get user's bookings
    user_bookings = db.execute('''
        SELECT b.*, c.name as cabin_name, c.cabin_number, c.image_url
        FROM bookings b
        JOIN cabins c ON b.cabin_id = c.id
        WHERE b.user_id = ?
        ORDER BY b.created_at DESC
        LIMIT 5
    ''', (session['user_id'],)).fetchall()
    
    return render_template('client_dashboard.html', cabins=cabins, bookings=user_bookings)

@app.route('/client/cabins')
@login_required
def client_cabins():
    db = get_db()
    cabins = db.execute('SELECT * FROM cabins ORDER BY price_per_night').fetchall()
    return render_template('client_cabins.html', cabins=cabins)

@app.route('/client/cabin/<int:cabin_id>')
@login_required
def cabin_detail(cabin_id):
    db = get_db()
    cabin = db.execute('SELECT * FROM cabins WHERE id = ?', (cabin_id,)).fetchone()
    
    if not cabin:
        flash('Cabin not found')
        return redirect(url_for('client_cabins'))
    
    # Get reviews for this cabin
    reviews = db.execute('''
        SELECT r.*, u.name as user_name
        FROM reviews r
        JOIN users u ON r.user_id = u.id
        WHERE r.cabin_id = ?
        ORDER BY r.created_at DESC
    ''', (cabin_id,)).fetchall()
    
    return render_template('cabin_detail.html', cabin=cabin, reviews=reviews)

@app.route('/client/cabin/<int:cabin_id>/book', methods=['GET', 'POST'])
@login_required
def book_cabin(cabin_id):
    db = get_db()
    cabin = db.execute('SELECT * FROM cabins WHERE id = ?', (cabin_id,)).fetchone()
    
    if not cabin:
        flash('Cabin not found')
        return redirect(url_for('client_cabins'))
    
    if request.method == 'POST':
        check_in = request.form.get('check_in')
        check_out = request.form.get('check_out')
        guests = request.form.get('guests')
        observations = request.form.get('observations', '')
        breakfast_included = 'breakfast_included' in request.form
        
        # Validate inputs
        if not check_in or not check_out or not guests:
            flash('Please fill in all required fields')
            return redirect(url_for('book_cabin', cabin_id=cabin_id))
        
        # Calculate nights and total price
        try:
            check_in_date = datetime.strptime(check_in, '%Y-%m-%d')
            check_out_date = datetime.strptime(check_out, '%Y-%m-%d')
            num_nights = (check_out_date - check_in_date).days
            
            if num_nights <= 0:
                flash('Check-out date must be after check-in date')
                return redirect(url_for('book_cabin', cabin_id=cabin_id))
            
            cabin_price = float(cabin['price_per_night']) * num_nights
            breakfast_price = 15 * num_nights * int(guests) if breakfast_included else 0
            total_price = cabin_price + breakfast_price
            
            # Check if cabin is available
            conflicting_bookings = db.execute('''
                SELECT COUNT(*) as count FROM bookings 
                WHERE cabin_id = ? 
                AND status IN ("unconfirmed", "checked_in")
                AND (
                    (check_in <= ? AND check_out >= ?)
                    OR (check_in <= ? AND check_out >= ?)
                    OR (check_in >= ? AND check_out <= ?)
                )
            ''', (cabin_id, check_in, check_in, check_out, check_out, check_in, check_out)).fetchone()
            
            if conflicting_bookings['count'] > 0:
                flash('Cabin is not available for selected dates')
                return redirect(url_for('book_cabin', cabin_id=cabin_id))
            
            # Create booking
            db.execute('''
                INSERT INTO bookings (user_id, cabin_id, check_in, check_out, num_nights, 
                                    num_guests, observations, breakfast_included, total_price, status)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, "unconfirmed")
            ''', (session['user_id'], cabin_id, check_in, check_out, num_nights, 
                  guests, observations, breakfast_included, total_price))
            db.commit()
            
            flash('Booking created successfully!')
            return redirect(url_for('client_bookings'))
        except (ValueError, TypeError) as e:
            flash('Invalid date or booking information')
            return redirect(url_for('book_cabin', cabin_id=cabin_id))
    
    # Calculate min dates for form
    today = datetime.now().date()
    min_checkin = (today + timedelta(days=1)).isoformat()
    min_checkout = (today + timedelta(days=2)).isoformat()
    
    return render_template('book_cabin.html', cabin=cabin, min_checkin=min_checkin, min_checkout=min_checkout)

@app.route('/client/bookings')
@login_required
def client_bookings():
    db = get_db()
    
    bookings = db.execute('''
        SELECT b.*, c.name as cabin_name, c.cabin_number, c.image_url
        FROM bookings b
        JOIN cabins c ON b.cabin_id = c.id
        WHERE b.user_id = ?
        ORDER BY b.created_at DESC
    ''', (session['user_id'],)).fetchall()
    
    return render_template('client_bookings.html', bookings=bookings)

@app.route('/client/booking/<int:booking_id>')
@login_required
def client_booking_detail(booking_id):
    db = get_db()
    
    booking = db.execute('''
        SELECT b.*, c.name as cabin_name, c.cabin_number, c.price_per_night, c.image_url
        FROM bookings b
        JOIN cabins c ON b.cabin_id = c.id
        WHERE b.id = ? AND b.user_id = ?
    ''', (booking_id, session['user_id'])).fetchone()
    
    if not booking:
        flash('Booking not found')
        return redirect(url_for('client_bookings'))
    
    return render_template('client_booking_detail.html', booking=booking)

@app.route('/client/booking/<int:booking_id>/cancel', methods=['POST'])
@login_required
def cancel_booking(booking_id):
    db = get_db()
    
    # Verify booking belongs to user
    booking = db.execute('SELECT * FROM bookings WHERE id = ? AND user_id = ?', 
                        (booking_id, session['user_id'])).fetchone()
    
    if not booking:
        flash('Booking not found')
        return redirect(url_for('client_bookings'))
    
    db.execute('UPDATE bookings SET status = "cancelled" WHERE id = ?', (booking_id,))
    db.commit()
    
    flash('Booking cancelled successfully')
    return redirect(url_for('client_bookings'))

@app.route('/client/booking/<int:booking_id>/review', methods=['POST'])
@login_required
def add_review(booking_id):
    db = get_db()
    
    # Verify booking belongs to user and is completed
    booking = db.execute('''
        SELECT * FROM bookings 
        WHERE id = ? AND user_id = ? AND status = "checked_out"
    ''', (booking_id, session['user_id'])).fetchone()
    
    if not booking:
        flash('Cannot review this booking')
        return redirect(url_for('client_bookings'))
    
    rating = request.form.get('rating')
    comment = request.form.get('comment', '')
    
    # Check if review already exists
    existing_review = db.execute('''
        SELECT id FROM reviews WHERE booking_id = ?
    ''', (booking_id,)).fetchone()
    
    if existing_review:
        db.execute('''
            UPDATE reviews SET rating = ?, comment = ?
            WHERE booking_id = ?
        ''', (rating, comment, booking_id))
    else:
        db.execute('''
            INSERT INTO reviews (user_id, cabin_id, booking_id, rating, comment)
            VALUES (?, ?, ?, ?, ?)
        ''', (session['user_id'], booking['cabin_id'], booking_id, rating, comment))
    
    db.commit()
    flash('Review submitted successfully')
    return redirect(url_for('client_booking_detail', booking_id=booking_id))

if __name__ == '__main__':
    if not os.path.exists(DATABASE):
        init_db()
    app.run(debug=True)
