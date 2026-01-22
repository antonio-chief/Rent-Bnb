# Quick Start Guide

## Running the Application

1. **Double-click** `start.bat` OR run the following command in terminal:
   ```
   python app.py
   ```

2. **Open your browser** and navigate to:
   ```
   http://localhost:5000
   ```

## Login Credentials

### Admin Dashboard
- Email: `admin@wildoasis.com`
- Password: `admin123`

### Client Dashboard
- Email: `test@gmail.com`
- Password: `client123`

## What You Can Do

### As a Client:
1. ✅ Sign up for a new account
2. ✅ Browse available cabins
3. ✅ View cabin details and reviews
4. ✅ Make a booking with date selection and breakfast option
5. ✅ View all your bookings
6. ✅ Cancel unconfirmed bookings
7. ✅ Leave reviews after checkout

### As an Admin:
1. ✅ View dashboard with key statistics
2. ✅ See today's arrivals
3. ✅ View and filter all bookings
4. ✅ Check guests in and out
5. ✅ Add new cabin properties
6. ✅ Edit existing cabins
7. ✅ Delete cabins or bookings
8. ✅ View all registered users

## Features

✅ **Fully Functional** - Complete booking flow from signup to review
✅ **Separate Dashboards** - Different interfaces for clients and admins
✅ **SQLite Database** - All data persisted in `rentbnb.db`
✅ **Secure Authentication** - Password hashing and role-based access
✅ **Beautiful UI** - Modern design matching the provided samples
✅ **Booking Management** - Date validation and availability checking
✅ **Review System** - Clients can rate and review cabins

## Database Tables

- **users** - Client and admin accounts
- **cabins** - Property listings (5 pre-loaded)
- **bookings** - Reservations with all details
- **reviews** - Guest feedback and ratings

## Application Structure

```
RentBnb/
├── app.py              - Main Flask application with all routes
├── schema.sql          - Database schema and sample data
├── rentbnb.db          - SQLite database (auto-created)
├── requirements.txt    - Python dependencies
├── README.md           - Detailed documentation
├── QUICKSTART.md       - This file
├── start.bat           - Windows launcher script
└── templates/          - All HTML templates (17 files)
```

## Stopping the Application

Press `Ctrl+C` in the terminal to stop the server.

## Troubleshooting

**If the app doesn't start:**
- Make sure Flask is installed: `pip install Flask`
- Check if port 5000 is already in use
- Ensure you're in the correct directory

**If you can't login:**
- Use the exact email and password provided above
- Password is case-sensitive

**If database errors occur:**
- Delete `rentbnb.db` and restart the app
- It will recreate the database automatically

## Next Steps

1. Try logging in as both admin and client
2. Create a new user account via signup
3. Browse cabins and make a test booking
4. As admin, check in the guest
5. As admin, check out the guest
6. As client, leave a review

Enjoy exploring The Wild Oasis booking system! 🏡
