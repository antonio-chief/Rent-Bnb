# 🎉 The Wild Oasis - Room Booking Application
## ✅ Project Complete!

---

## 📋 Project Summary

I've successfully built a **fully functional room booking application** based on your requirements and the provided design images. The application features separate dashboards for clients and administrators, complete booking functionality, user authentication, and a review system.

---

## 🚀 Quick Start

### **Application is Currently Running!**
- **URL**: http://localhost:5000
- **Status**: ✅ Server is running on port 5000

### Login Credentials

#### 👨‍💼 Admin Account
- **Email**: admin@wildoasis.com
- **Password**: admin123

#### 👤 Client Account  
- **Email**: test@gmail.com
- **Password**: client123

---

## ✨ Features Implemented

### 🔐 Authentication System
- ✅ User signup with password hashing
- ✅ Secure login system
- ✅ Role-based access control (admin/client)
- ✅ Session management
- ✅ Automatic redirect to appropriate dashboard

### 👥 Client Features
- ✅ Personal dashboard with booking overview
- ✅ Browse all available cabins
- ✅ View detailed cabin information
- ✅ Make bookings with:
  - Date selection (check-in/check-out)
  - Guest count
  - Optional breakfast ($15/person/night)
  - Special requests/observations
  - Real-time price calculation
- ✅ View all personal bookings
- ✅ Cancel unconfirmed bookings
- ✅ Leave reviews after checkout (star rating + comment)

### 🏢 Admin Features
- ✅ Comprehensive dashboard with analytics:
  - Total bookings count
  - Total sales revenue
  - Check-ins count
  - Occupancy rate percentage
  - Today's arrivals list
  - Recent bookings
- ✅ All bookings management:
  - View all bookings
  - Filter by status (all/checked out/checked in/unconfirmed)
  - Detailed booking view
  - Check guests in
  - Check guests out
  - Delete bookings
- ✅ Property/Cabin management:
  - Add new cabins
  - Edit cabin details
  - Delete cabins
  - View all properties
- ✅ User management:
  - View all registered users
  - See user roles and join dates

### 🗄️ Database
- ✅ SQLite database (`rentbnb.db`)
- ✅ Four main tables:
  - **users** - Client and admin accounts
  - **cabins** - Property listings
  - **bookings** - Reservation records
  - **reviews** - Guest feedback
- ✅ Pre-loaded with:
  - 1 admin user
  - 1 test client user
  - 5 sample cabin properties

### 🎨 Design
- ✅ Modern, clean UI matching provided images
- ✅ Responsive layout with sidebar navigation
- ✅ Card-based design system
- ✅ Color-coded status badges
- ✅ Interactive forms with validation
- ✅ Hover effects and transitions
- ✅ Professional color scheme (indigo/blue theme)

---

## 📁 Project Structure

```
RentBnb/
├── app.py                         # Main Flask application (600+ lines)
├── schema.sql                     # Database schema with sample data
├── rentbnb.db                     # SQLite database (auto-created)
├── requirements.txt               # Python dependencies
├── README.md                      # Full documentation
├── QUICKSTART.md                  # Quick start guide
├── start.bat                      # Windows launcher
└── templates/                     # HTML templates (17 files)
    ├── base.html                  # Base template with navigation
    ├── login.html                 # Login page
    ├── signup.html                # Registration page
    ├── admin_dashboard.html       # Admin home with stats
    ├── admin_bookings.html        # All bookings view
    ├── admin_booking_detail.html  # Booking details for admin
    ├── admin_cabins.html          # Cabin management
    ├── admin_add_cabin.html       # Add new cabin form
    ├── admin_edit_cabin.html      # Edit cabin form
    ├── admin_users.html           # User management
    ├── client_dashboard.html      # Client home
    ├── client_cabins.html         # Browse cabins
    ├── cabin_detail.html          # Cabin details with reviews
    ├── book_cabin.html            # Booking form
    ├── client_bookings.html       # My bookings list
    └── client_booking_detail.html # Booking details with review form
```

---

## 🔄 Complete User Flows

### Client Journey
1. **Sign Up** → Create account with name, email, password
2. **Login** → Automatic redirect to client dashboard
3. **Browse Cabins** → View all available properties
4. **View Details** → See cabin information, amenities, reviews
5. **Book Cabin** → Select dates, guests, add breakfast, confirm
6. **View Bookings** → Track all reservations
7. **Manage Booking** → View details, cancel if needed
8. **Leave Review** → Rate and review after checkout

### Admin Journey
1. **Login** → Access admin dashboard
2. **View Analytics** → See bookings, sales, occupancy
3. **Today's Arrivals** → Quick view of check-ins
4. **Manage Bookings** → Check in/out guests
5. **Add Properties** → Create new cabin listings
6. **Edit Cabins** → Update property information
7. **View Users** → See all registered clients

---

## 🛠️ Technologies Used

- **Backend**: Flask 3.1.2 (Python web framework)
- **Database**: SQLite (lightweight, serverless)
- **Security**: Werkzeug password hashing
- **Frontend**: HTML5, CSS3, JavaScript
- **Template Engine**: Jinja2
- **Session Management**: Flask sessions

---

## 📊 Database Schema

### Users Table
- id, name, email, password (hashed), phone, national_id, role, created_at

### Cabins Table
- id, name, cabin_number, capacity, price_per_night, description, amenities, image_url, created_at

### Bookings Table
- id, user_id, cabin_id, check_in, check_out, num_nights, num_guests, observations, breakfast_included, total_price, status, created_at

### Reviews Table
- id, user_id, cabin_id, booking_id, rating (1-5), comment, created_at

---

## 🎯 Key Functionality Highlights

### Smart Booking System
- ✅ Automatic date validation
- ✅ Availability checking (no double bookings)
- ✅ Real-time price calculation
- ✅ Breakfast cost calculation ($15 × guests × nights)
- ✅ Multiple booking statuses tracking

### Admin Analytics
- ✅ Real-time statistics calculations
- ✅ Occupancy rate computation
- ✅ Today's arrivals filtering
- ✅ Sales revenue tracking

### Security Features
- ✅ Password hashing (never stored plain text)
- ✅ Session-based authentication
- ✅ Role-based access control
- ✅ Login required decorators
- ✅ Admin-only route protection

---

## 📖 How to Use

### Starting the Application
```bash
# Method 1: Double-click start.bat

# Method 2: Command line
python app.py
```

### Accessing the Application
1. Open browser
2. Go to: http://localhost:5000
3. You'll see the login page

### Testing Client Features
1. Login as: test@gmail.com / client123
2. Browse the 5 pre-loaded cabins
3. Make a test booking
4. View your bookings

### Testing Admin Features
1. Login as: admin@wildoasis.com / admin123
2. View dashboard statistics
3. Check in the test booking
4. Add a new cabin
5. View all users

---

## 🔧 Sample Data Included

### 5 Cabins Pre-loaded:
1. **Mountain View Cabin** - $250/night, 4 guests
2. **Lakeside Retreat** - $350/night, 6 guests
3. **Forest Haven** - $180/night, 2 guests
4. **Riverside Lodge** - $450/night, 8 guests
5. **Sunset Cabin** - $200/night, 3 guests

All include amenities like WiFi, Kitchen, and unique features.

---

## 🎨 Design Match

The application closely matches the provided design images:
- ✅ Login page with centered form and logo
- ✅ Dashboard with stats cards (bookings, sales, check-ins, occupancy)
- ✅ Bookings list with cabin, guest, dates, status, amount columns
- ✅ Booking detail page with guest info and pricing breakdown
- ✅ Clean sidebar navigation
- ✅ Color scheme: Indigo primary, status badges
- ✅ Card-based layouts
- ✅ Professional typography

---

## 🚦 Next Steps (Future Enhancements)

While the application is fully functional, here are potential improvements:

1. **Payment Integration** - Stripe/PayPal for online payments
2. **Email Notifications** - Booking confirmations and reminders
3. **Image Upload** - Allow admins to upload cabin photos
4. **Calendar View** - Visual booking calendar
5. **Advanced Search** - Filter by price, capacity, amenities
6. **Reports** - Generate PDF booking reports
7. **Multi-language** - Internationalization support
8. **Mobile App** - Native iOS/Android apps
9. **SMS Notifications** - Text message alerts
10. **Ratings Analytics** - Average rating per cabin

---

## ⚠️ Important Notes

### Security
- Change `app.secret_key` before production deployment
- Use environment variables for sensitive data
- Implement HTTPS in production
- Add rate limiting for login attempts

### Production Deployment
- Use a production WSGI server (Gunicorn, uWSGI)
- Switch to PostgreSQL or MySQL for better scalability
- Add proper error handling and logging
- Implement database backups
- Add monitoring and alerting

---

## 📝 Testing Checklist

✅ User signup works
✅ Login with correct credentials
✅ Login with wrong credentials fails
✅ Admin sees admin dashboard
✅ Client sees client dashboard
✅ Browse cabins works
✅ View cabin details shows info
✅ Make booking creates record
✅ View bookings shows user's bookings
✅ Cancel booking updates status
✅ Admin can check in guests
✅ Admin can check out guests
✅ Reviews can be submitted after checkout
✅ Admin can add new cabins
✅ Admin can edit cabins
✅ Admin can delete cabins
✅ Price calculation works correctly
✅ Date validation prevents invalid bookings
✅ Logout clears session

---

## 🎓 Learning Resources

This project demonstrates:
- Flask web framework usage
- SQLite database operations
- User authentication and authorization
- Session management
- Form handling and validation
- Template rendering with Jinja2
- RESTful routing
- CSS styling and layout
- JavaScript for interactivity
- Role-based access control

---

## 📧 Support

If you encounter any issues:
1. Check the terminal for error messages
2. Verify database exists (rentbnb.db)
3. Ensure Flask is installed
4. Check port 5000 is available
5. Review README.md for detailed documentation

---

## 🏆 Project Status: COMPLETE ✅

All requested features have been implemented:
- ✅ Client login and signup
- ✅ Room reservation functionality
- ✅ Admin view reservations
- ✅ Admin add properties
- ✅ Fully functional booking flow
- ✅ Review system
- ✅ SQLite database
- ✅ Design based on sample images
- ✅ Separate client and admin dashboards

---

**Developed with Flask • SQLite • Python**

**Ready to use! Open http://localhost:5000 in your browser.** 🚀
