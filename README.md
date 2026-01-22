# The Wild Oasis - Room Booking Application

A fully functional room booking application built with Flask and SQLite, featuring separate dashboards for clients and administrators.

## Features

### Client Features
- **User Registration & Login**: Secure signup and authentication system
- **Browse Cabins**: View all available properties with details
- **Make Reservations**: Book cabins with date selection, guest count, and optional breakfast
- **Manage Bookings**: View, track, and cancel reservations
- **Leave Reviews**: Rate and review cabins after checkout

### Admin Features
- **Dashboard Analytics**: View bookings, sales, check-ins, and occupancy rate
- **Booking Management**: View all bookings, check guests in/out, manage reservations
- **Property Management**: Add, edit, and delete cabin listings
- **User Management**: View all registered users
- **Today's Arrivals**: Quick view of guests checking in today

## Installation

1. **Install Python dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

2. **Run the application**:
   ```bash
   python app.py
   ```

3. The application will automatically create the SQLite database on first run.

4. Open your browser and navigate to:
   ```
   http://localhost:5000
   ```

## Default Accounts

### Admin Account
- **Email**: admin@wildoasis.com
- **Password**: admin123

### Client Account
- **Email**: test@gmail.com
- **Password**: client123

## Database Schema

The application uses SQLite with the following tables:

- **users**: User accounts (clients and admins)
- **cabins**: Property listings
- **bookings**: Reservations with dates, guests, and pricing
- **reviews**: Guest reviews for cabins

## Application Structure

```
RentBnb/
├── app.py                 # Main Flask application
├── schema.sql            # Database schema
├── requirements.txt      # Python dependencies
├── rentbnb.db           # SQLite database (auto-created)
└── templates/           # HTML templates
    ├── base.html                    # Base template
    ├── login.html                   # Login page
    ├── signup.html                  # Registration page
    ├── admin_dashboard.html         # Admin home
    ├── admin_bookings.html          # All bookings view
    ├── admin_booking_detail.html    # Single booking details
    ├── admin_cabins.html            # Cabin management
    ├── admin_add_cabin.html         # Add new cabin
    ├── admin_edit_cabin.html        # Edit cabin
    ├── admin_users.html             # User management
    ├── client_dashboard.html        # Client home
    ├── client_cabins.html           # Browse cabins
    ├── cabin_detail.html            # Cabin details
    ├── book_cabin.html              # Booking form
    ├── client_bookings.html         # My bookings
    └── client_booking_detail.html   # Booking details with review
```

## Key Functionalities

### Authentication
- Separate login paths for clients and admins
- Password hashing with Werkzeug
- Session-based authentication
- Role-based access control

### Booking System
- Date validation and availability checking
- Automatic price calculation
- Optional breakfast add-on
- Multiple booking statuses: unconfirmed, checked_in, checked_out, cancelled

### Admin Dashboard
- Real-time statistics
- Today's arrivals section
- Sales and occupancy tracking
- Full CRUD operations for properties

### Client Dashboard
- Property browsing with filters
- Detailed cabin information
- Booking history
- Review submission after checkout

## Technologies Used

- **Backend**: Flask (Python web framework)
- **Database**: SQLite
- **Authentication**: Werkzeug Security
- **Frontend**: HTML, CSS (embedded), JavaScript
- **Template Engine**: Jinja2

## Usage Guide

### For Clients:

1. **Sign Up**: Create a new account with name, email, and password
2. **Browse Cabins**: View available properties on the dashboard or cabins page
3. **Book a Cabin**: 
   - Select a cabin
   - Choose check-in/check-out dates
   - Specify number of guests
   - Add optional breakfast
   - Confirm booking
4. **Manage Bookings**: View all your bookings and their status
5. **Leave Review**: After checking out, submit a rating and review

### For Admins:

1. **Login**: Use admin credentials
2. **View Dashboard**: See key metrics and today's arrivals
3. **Manage Bookings**: 
   - View all bookings
   - Check guests in/out
   - Delete bookings if needed
4. **Manage Properties**:
   - Add new cabins with details and pricing
   - Edit existing cabin information
   - Remove cabins from listings
5. **View Users**: Access list of all registered users

## Sample Data

The application comes pre-loaded with:
- 5 sample cabins with different capacities and price points
- 1 admin user
- 1 client user for testing

## Security Notes

- Change the `app.secret_key` in production
- Use environment variables for sensitive data
- Implement HTTPS in production
- Add rate limiting for authentication endpoints
- Consider adding email verification

## Future Enhancements

- Payment integration
- Email notifications
- Advanced search and filtering
- Booking calendar view
- Image upload for cabins
- Multi-language support
- Mobile responsive improvements

## License

This project is for educational purposes.
