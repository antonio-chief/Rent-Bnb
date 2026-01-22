# RentBnb - System Design Document

## Table of Contents
1. [System Overview](#system-overview)
2. [Architecture Design](#architecture-design)
3. [Layer Communication](#layer-communication)
4. [Database Schema](#database-schema)
5. [API/Service Interface](#apiservice-interface)
6. [Client-Server Interaction](#client-server-interaction)
7. [Reliability, Fault Tolerance & Scalability](#reliability-fault-tolerance--scalability)
8. [Security Considerations](#security-considerations)
9. [Future Enhancements](#future-enhancements)

---

## System Overview

**RentBnb** is a cabin rental management system that facilitates property bookings between guests (clients) and property managers (admins). The system provides:

- **Client Features**: Browse cabins, make bookings, view booking history, submit reviews
- **Admin Features**: Manage cabins, view/manage bookings, track users, dashboard analytics
- **Core Functionality**: Availability checking, pricing calculation, file upload management

### Technology Stack
- **Backend Framework**: Flask (Python 3.x)
- **Database**: SQLite (Development), PostgreSQL/MySQL recommended for production
- **Frontend**: Jinja2 Templates, HTML5, CSS3, JavaScript
- **Security**: Werkzeug password hashing, session management
- **File Storage**: Local filesystem (static/uploads)

---

## Architecture Design

### High-Level Architecture Diagram

┌─────────────────────────────────────────────────────────────────┐
│                         CLIENT TIER                              │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐          │
│  │   Web Browser │  │   Mobile     │  │    Tablet    │          │
│  │   (Chrome,    │  │   Browser    │  │    Browser   │          │
│  │   Firefox,    │  │              │  │              │          │
│  │   Safari)     │  │              │  │              │          │
│  └──────┬───────┘  └──────┬───────┘  └──────┬───────┘          │
│         │                  │                  │                   │
│         └─```
─────────────────┼──────────────────┘                   │
│                            │                                      │
└────────────────────────────┼──────────────────────────────────────┘
                             │ HTTP/HTTPS
                             │ (HTML, CSS, JS, Form Data)
┌────────────────────────────┼──────────────────────────────────────┐
│                         WEB TIER                                  │
│  ┌──────────────────────────────────────────────────────────┐    │
│  │           Flask Application Server (WSGI)                 │    │
│  │                                                            │    │
│  │  ┌─────────────────────────────────────────────────────┐ │    │
│  │  │           PRESENTATION LAYER                         │ │    │
│  │  │  • Route Handlers                                    │ │    │
│  │  │  • Template Rendering (Jinja2)                       │ │    │
│  │  │  • Static File Serving                               │ │    │
│  │  │  • Session Management                                │ │    │
│  │  └─────────────────┬───────────────────────────────────┘ │    │
│  │                    │                                      │    │
│  │  ┌─────────────────▼───────────────────────────────────┐ │    │
│  │  │           BUSINESS LOGIC LAYER                       │ │    │
│  │  │  • Authentication & Authorization                    │ │    │
│  │  │  • Booking Management Logic                          │ │    │
│  │  │  • Availability Validation                           │ │    │
│  │  │  • Price Calculation                                 │ │    │
│  │  │  • File Upload Processing                            │ │    │
│  │  │  • Review Management                                 │ │    │
│  │  └─────────────────┬───────────────────────────────────┘ │    │
│  │                    │                                      │    │
│  │  ┌─────────────────▼───────────────────────────────────┐ │    │
│  │  │           DATA ACCESS LAYER                          │ │    │
│  │  │  • Database Connection Pool                          │ │    │
│  │  │  • SQL Query Execution                               │ │    │
│  │  │  • Transaction Management                            │ │    │
│  │  │  • Data Mapping (Row Factory)                        │ │    │
│  │  └─────────────────┬───────────────────────────────────┘ │    │
│  └────────────────────┼───────────────────────────────────────┘    │
└────────────────────────┼──────────────────────────────────────┘
                         │ SQL Queries
┌────────────────────────┼──────────────────────────────────────┐
│                    DATA TIER                                   │
│  ┌──────────────────────────────────────────────────────────┐ │
│  │           SQLite Database (rentbnb.db)                    │ │
│  │  ┌─────────┐  ┌─────────┐  ┌─────────┐  ┌─────────┐    │ │
│  │  │  Users  │  │ Cabins  │  │Bookings │  │ Reviews │    │ │
│  │  │  Table  │  │  Table  │  │  Table  │  │  Table  │    │ │
│  │  └─────────┘  └─────────┘  └─────────┘  └─────────┘    │ │
│  └──────────────────────────────────────────────────────────┘ │
│  ┌──────────────────────────────────────────────────────────┐ │
│  │           File Storage System                             │ │
│  │  static/uploads/ (Cabin Images)                           │ │
│  └──────────────────────────────────────────────────────────┘ │
└────────────────────────────────────────────────────────────────┘
```

### Architectural Pattern
The system follows a **Layered (N-Tier) Architecture** with three primary layers:

1. **Presentation Layer**: Handles HTTP requests, renders templates, manages sessions
2. **Business Logic Layer**: Implements business rules, validation, and orchestration
3. **Data Access Layer**: Manages database interactions and data persistence

---

## Layer Communication

### Communication Flow

```
┌─────────────────────────────────────────────────────────────────┐
│                    LAYER COMMUNICATION FLOW                      │
└─────────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────────┐
│  1. CLIENT REQUEST                                               │
│     User → Browser → HTTP POST /client/cabin/5/book             │
└─────────────────────┬───────────────────────────────────────────┘
                      │
                      ▼
┌─────────────────────────────────────────────────────────────────┐
│  2. PRESENTATION LAYER (app.py - Route Handler)                  │
│     @app.route('/client/cabin/<int:cabin_id>/book')             │
│     @login_required                                              │
│     def book_cabin(cabin_id):                                    │
│         ├─ Validate session (login_required decorator)          │
│         ├─ Extract form data (request.form)                     │
│         └─ Pass to Business Logic Layer ──────────┐             │
└───────────────────────────────────────────────────┼─────────────┘
                                                    │
                                                    ▼
┌─────────────────────────────────────────────────────────────────┐
│  3. BUSINESS LOGIC LAYER (app.py - Function Logic)              │
│     ├─ Parse dates and validate format                          │
│     ├─ Calculate nights: (checkout - checkin).days              │
│     ├─ Calculate total price:                                   │
│     │    cabin_price = price_per_night × nights                 │
│     │    breakfast = 15 × nights × guests (if selected)         │
│     │    total = cabin_price + breakfast                        │
│     ├─ Validate business rules:                                 │
│     │    • Check-out must be after check-in                     │
│     │    • Guests ≤ Cabin capacity                              │
│     ├─ Check availability (call Data Layer) ───────┐            │
│     └─ If valid, create booking (call Data Layer) ─┼─┐          │
└────────────────────────────────────────────────────┼─┼──────────┘
                                                     │ │
                                                     ▼ ▼
┌─────────────────────────────────────────────────────────────────┐
│  4. DATA ACCESS LAYER (get_db() + SQL Queries)                  │
│     db = get_db()  # Create connection with row_factory          │
│                                                                   │
│     A. Availability Check Query:                                 │
│        SELECT COUNT(*) FROM bookings WHERE                       │
│          cabin_id = ? AND status IN (...)                        │
│          AND (date overlaps logic)                               │
│        Returns: count of conflicts                               │
│                                                                   │
│     B. Create Booking Query:                                     │
│        INSERT INTO bookings (user_id, cabin_id, ...)             │
│        VALUES (?, ?, ...)                                        │
│        db.commit()  # Persist transaction                        │
│                                                                   │
│     └─ Return result to Business Layer ────────────┐             │
└────────────────────────────────────────────────────┼─────────────┘
                                                     │
                                                     ▼
┌─────────────────────────────────────────────────────────────────┐
│  5. DATABASE TIER (SQLite)                                       │
│     ├─ Execute SQL statements                                   │
│     ├─ Enforce constraints (foreign keys, uniqueness)           │
│     ├─ Apply transactions (ACID properties)                     │
│     └─ Return result sets ──────────────────────┐               │
└─────────────────────────────────────────────────┼───────────────┘
                                                  │
                    ┌─────────────────────────────┘
                    │
                    ▼
┌─────────────────────────────────────────────────────────────────┐
│  6. RESPONSE FLOW (Bottom to Top)                               │
│     Database → Data Layer → Business Layer → Presentation       │
│     ├─ If success: flash('Booking created successfully!')       │
│     │              redirect(url_for('client_bookings'))         │
│     └─ If error:   flash('Error message')                       │
│                    redirect back to form                         │
└─────────────────────┬───────────────────────────────────────────┘
                      │
                      ▼
┌─────────────────────────────────────────────────────────────────┐
│  7. CLIENT RESPONSE                                              │
│     Browser ← HTTP 302 Redirect → New Page Rendered             │
└─────────────────────────────────────────────────────────────────┘
```

### Key Communication Principles

1. **Unidirectional Flow**: Requests flow downward (Client → Presentation → Logic → Data → DB), responses flow upward
2. **Separation of Concerns**: Each layer has a specific responsibility
3. **Dependency Direction**: Higher layers depend on lower layers, not vice versa
4. **Data Transformation**: Each layer transforms data into appropriate formats
5. **Error Propagation**: Errors bubble up from lower layers to presentation layer for user feedback

---

## Database Schema

### Entity-Relationship Diagram (ERD)

```
┌─────────────────────────────────────────────────────────────────┐
│                    DATABASE SCHEMA (ERD)                         │
└─────────────────────────────────────────────────────────────────┘

┌───────────────────────────┐
│         USERS             │
├───────────────────────────┤
│ PK  id (INT)              │
│     name (TEXT)           │
│ UK  email (TEXT)          │
│     password (TEXT)       │──────────┐
│     phone (TEXT)          │          │
│     national_id (TEXT)    │          │ 1 User
│     role (TEXT)           │          │ creates many
│     created_at (TIMESTAMP)│          │ Bookings
└───────────────┬───────────┘          │
                │                      │
                │ 1 User               │
                │ submits many         │
                │ Reviews              │
                │                      │
                └──────┐               │
                       │               │
┌──────────────────────┼───────────────┼──────────────────────────┐
│         CABINS       │               │                          │
├──────────────────────┼───────────────┼──────────────────────────┤
│ PK  id (INT)         │               │                          │
│     name (TEXT)      │               │                          │
│ UK  cabin_number     │◄──────┐       │                          │
│     (TEXT)           │       │       │                          │
│     capacity (INT)   │       │ M     │ M                        │
│     price_per_night  │       │ Cabins│ Bookings                 │
│     (REAL)           │       │ receive│ belong to               │
│     description (TEXT)│      │ many  │ 1 Cabin                  │
│     amenities (TEXT) │       │Bookings│                         │
│     image_url (TEXT) │       │       │                          │
│     created_at       │       │       │                          │
│     (TIMESTAMP)      │       │       │                          │
└──────────────┬───────┘       │       │                          │
               │               │       │                          │
               │ 1 Cabin       │       │                          │
               │ has many      │       │                          │
               │ Reviews       │       │                          │
               │               │       │                          │
               └──────┐        │       │                          │
                      │        │       │                          │
         ┌────────────┼────────┼───────┼────────────────────┐     │
         │  BOOKINGS  │        │       │                    │     │
         ├────────────┼────────┼───────┼────────────────────┤     │
         │ PK  id (INT)        │       │                    │     │
         │ FK  user_id (INT)   │◄──────┘                    │     │
         │ FK  cabin_id (INT)  │◄──────────────────────────┐│     │
         │     check_in (DATE) │                            ││     │
         │     check_out (DATE)│                            ││     │
         │     num_nights (INT)│                            ││     │
         │     num_guests (INT)│                            ││     │
         │     observations    │                            ││     │
         │     (TEXT)          │                            ││     │
         │     breakfast_       │                           ││     │
         │     included (BOOL) │                            ││     │
         │     total_price     │                            ││     │
         │     (REAL)          │                            ││     │
         │     status (TEXT)   │───────┐                    ││     │
         │     created_at      │       │                    ││     │
         │     (TIMESTAMP)     │       │ 1 Booking         ││     │
         └─────────────────────┘       │ has 0..1          ││     │
                                       │ Review            ││     │
                                       │                   ││     │
         ┌─────────────────────────────┼───────────────────┼┼─────┼┐
         │  REVIEWS                    │                   ││     ││
         ├─────────────────────────────┼───────────────────┼┼─────┼┤
         │ PK  id (INT)                │                   ││     ││
         │ FK  user_id (INT)           │◄──────────────────┘│     ││
         │ FK  cabin_id (INT)          │◄───────────────────┘     ││
         │ FK  booking_id (INT)        │◄──────────────────────────┘│
         │     rating (INT)            │                            │
         │     CHECK (1 <= rating <= 5)│                            │
         │     comment (TEXT)          │                            │
         │     created_at (TIMESTAMP)  │                            │
         └─────────────────────────────┘                            │
                                                                    │
LEGEND:                                                             │
  PK = Primary Key                                                  │
  FK = Foreign Key                                                  │
  UK = Unique Key                                                   │
```

### Table Definitions

#### 1. **USERS Table**
Stores user account information for both clients and administrators.

| Column      | Type      | Constraints           | Description                    |
|-------------|-----------|-----------------------|--------------------------------|
| id          | INTEGER   | PRIMARY KEY, AUTO_INC | Unique user identifier         |
| name        | TEXT      | NOT NULL              | Full name of the user          |
| email       | TEXT      | UNIQUE, NOT NULL      | Login email (unique)           |
| password    | TEXT      | NOT NULL              | Hashed password (Werkzeug)     |
| phone       | TEXT      | NULL                  | Contact phone number           |
| national_id | TEXT      | NULL                  | Government ID for verification |
| role        | TEXT      | NOT NULL, DEFAULT     | 'client' or 'admin'            |
| created_at  | TIMESTAMP | DEFAULT CURRENT_TS    | Account creation timestamp     |

**Indexes:**
- PRIMARY INDEX on `id`
- UNIQUE INDEX on `email`
- INDEX on `role` (for filtering)

---

#### 2. **CABINS Table**
Stores rental property information.

| Column          | Type      | Constraints           | Description                    |
|-----------------|-----------|-----------------------|--------------------------------|
| id              | INTEGER   | PRIMARY KEY, AUTO_INC | Unique cabin identifier        |
| name            | TEXT      | NOT NULL              | Display name of cabin          |
| cabin_number    | TEXT      | UNIQUE, NOT NULL      | Cabin identifier (e.g., "001") |
| capacity        | INTEGER   | NOT NULL              | Maximum guest capacity         |
| price_per_night | REAL      | NOT NULL              | Nightly rental rate (USD)      |
| description     | TEXT      | NULL                  | Detailed description           |
| amenities       | TEXT      | NULL                  | Comma-separated amenities      |
| image_url       | TEXT      | NULL                  | Path or URL to cabin image     |
| created_at      | TIMESTAMP | DEFAULT CURRENT_TS    | Record creation timestamp      |

**Indexes:**
- PRIMARY INDEX on `id`
- UNIQUE INDEX on `cabin_number`
- INDEX on `price_per_night` (for sorting/filtering)

---

#### 3. **BOOKINGS Table**
Stores reservation information.

| Column             | Type      | Constraints           | Description                     |
|--------------------|-----------|-----------------------|---------------------------------|
| id                 | INTEGER   | PRIMARY KEY, AUTO_INC | Unique booking identifier       |
| user_id            | INTEGER   | FOREIGN KEY, NOT NULL | Reference to users.id           |
| cabin_id           | INTEGER   | FOREIGN KEY, NOT NULL | Reference to cabins.id          |
| check_in           | DATE      | NOT NULL              | Check-in date                   |
| check_out          | DATE      | NOT NULL              | Check-out date                  |
| num_nights         | INTEGER   | NOT NULL              | Calculated: checkout - checkin  |
| num_guests         | INTEGER   | NOT NULL              | Number of guests                |
| observations       | TEXT      | NULL                  | Special requests/notes          |
| breakfast_included | BOOLEAN   | DEFAULT 0             | Breakfast add-on selection      |
| total_price        | REAL      | NOT NULL              | Total calculated price          |
| status             | TEXT      | NOT NULL, DEFAULT     | Booking status (see below)      |
| created_at         | TIMESTAMP | DEFAULT CURRENT_TS    | Booking creation timestamp      |

**Status Values:**
- `unconfirmed`: Booking created, awaiting check-in
- `checked_in`: Guest has arrived
- `checked_out`: Guest has departed
- `cancelled`: Booking cancelled by client/admin

**Indexes:**
- PRIMARY INDEX on `id`
- INDEX on `user_id` (for user booking queries)
- INDEX on `cabin_id` (for availability checks)
- COMPOSITE INDEX on `(cabin_id, check_in, check_out, status)` (for availability queries)
- INDEX on `status` (for filtering)

**Foreign Keys:**
- `user_id` → `users(id)` (ON DELETE CASCADE)
- `cabin_id` → `cabins(id)` (ON DELETE CASCADE)

---

#### 4. **REVIEWS Table**
Stores guest reviews for cabins after checkout.

| Column     | Type      | Constraints                    | Description                   |
|------------|-----------|--------------------------------|-------------------------------|
| id         | INTEGER   | PRIMARY KEY, AUTO_INC          | Unique review identifier      |
| user_id    | INTEGER   | FOREIGN KEY, NOT NULL          | Reference to users.id         |
| cabin_id   | INTEGER   | FOREIGN KEY, NOT NULL          | Reference to cabins.id        |
| booking_id | INTEGER   | FOREIGN KEY, NOT NULL          | Reference to bookings.id      |
| rating     | INTEGER   | NOT NULL, CHECK (1-5)          | Star rating (1-5)             |
| comment    | TEXT      | NULL                           | Written review                |
| created_at | TIMESTAMP | DEFAULT CURRENT_TS             | Review submission timestamp   |

**Indexes:**
- PRIMARY INDEX on `id`
- INDEX on `cabin_id` (for cabin review lookups)
- UNIQUE INDEX on `booking_id` (one review per booking)

**Foreign Keys:**
- `user_id` → `users(id)` (ON DELETE CASCADE)
- `cabin_id` → `cabins(id)` (ON DELETE CASCADE)
- `booking_id` → `bookings(id)` (ON DELETE CASCADE)

---

### Relationships

| Relationship           | Cardinality | Description                                    |
|------------------------|-------------|------------------------------------------------|
| Users → Bookings       | 1:M         | One user can make many bookings                |
| Cabins → Bookings      | 1:M         | One cabin can have many bookings               |
| Bookings → Reviews     | 1:0..1      | One booking can have zero or one review        |
| Users → Reviews        | 1:M         | One user can write many reviews                |
| Cabins → Reviews       | 1:M         | One cabin can receive many reviews             |

---

## API/Service Interface

### HTTP Endpoint Specification

#### Authentication Endpoints

| Method | Endpoint      | Description          | Auth Required | Request Body                                      | Response                        |
|--------|---------------|----------------------|---------------|---------------------------------------------------|---------------------------------|
| GET    | `/login`      | Display login form   | No            | N/A                                               | HTML (login.html)               |
| POST   | `/login`      | Authenticate user    | No            | `email`, `password`                               | Redirect to dashboard           |
| GET    | `/signup`     | Display signup form  | No            | N/A                                               | HTML (signup.html)              |
| POST   | `/signup`     | Register new user    | No            | `name`, `email`, `password`, `phone`, `role`      | Redirect to login               |
| GET    | `/logout`     | End user session     | No            | N/A                                               | Redirect to login               |

---

#### Admin Endpoints

**Dashboard & Analytics**

| Method | Endpoint            | Description             | Auth Required | Query Params | Response                |
|--------|---------------------|-------------------------|---------------|--------------|-------------------------|
| GET    | `/admin/dashboard`  | Admin dashboard         | Admin         | N/A          | HTML with stats         |
| GET    | `/admin/users`      | List all users          | Admin         | N/A          | HTML (users table)      |

**Booking Management**

| Method | Endpoint                           | Description           | Auth Required | Request Body | Response                |
|--------|------------------------------------|----------------------|---------------|--------------|-------------------------|
| GET    | `/admin/bookings`                  | List all bookings     | Admin         | `status=all` | HTML (bookings table)   |
| GET    | `/admin/booking/<int:booking_id>`  | View booking details  | Admin         | N/A          | HTML (booking detail)   |
| POST   | `/admin/booking/<int:booking_id>/check-in` | Check in guest | Admin  | N/A          | Redirect to detail      |
| POST   | `/admin/booking/<int:booking_id>/check-out`| Check out guest| Admin  | N/A          | Redirect to detail      |
| POST   | `/admin/booking/<int:booking_id>/delete`   | Delete booking | Admin  | N/A          | Redirect to bookings    |

**Cabin Management**

| Method | Endpoint                           | Description           | Auth Required | Request Body                                              | Response                |
|--------|------------------------------------|----------------------|---------------|-----------------------------------------------------------|-------------------------|
| GET    | `/admin/cabins`                    | List all cabins       | Admin         | N/A                                                       | HTML (cabins table)     |
| GET    | `/admin/cabin/add`                 | Show add cabin form   | Admin         | N/A                                                       | HTML (add form)         |
| POST   | `/admin/cabin/add`                 | Create new cabin      | Admin         | `name`, `cabin_number`, `capacity`, `price_per_night`, `description`, `amenities`, `image_url`, `image_file` | Redirect to cabins      |
| GET    | `/admin/cabin/<int:cabin_id>/edit` | Show edit cabin form  | Admin         | N/A                                                       | HTML (edit form)        |
| POST   | `/admin/cabin/<int:cabin_id>/edit` | Update cabin          | Admin         | Same as add                                               | Redirect to cabins      |
| POST   | `/admin/cabin/<int:cabin_id>/delete` | Delete cabin        | Admin         | N/A                                                       | Redirect to cabins      |

---

#### Client Endpoints

**Dashboard & Cabin Browsing**

| Method | Endpoint                      | Description             | Auth Required | Response                |
|--------|-------------------------------|-------------------------|---------------|-------------------------|
| GET    | `/client/dashboard`           | Client dashboard        | Client        | HTML with cabins list   |
| GET    | `/client/cabins`              | Browse available cabins | Client        | HTML (cabin cards)      |
| GET    | `/client/cabin/<int:cabin_id>`| View cabin details      | Client        | HTML (cabin detail)     |

**Booking Management**

| Method | Endpoint                                   | Description            | Auth Required | Request Body                                              | Response                |
|--------|--------------------------------------------|------------------------|---------------|-----------------------------------------------------------|-------------------------|
| GET    | `/client/cabin/<int:cabin_id>/book`        | Show booking form      | Client        | N/A                                                       | HTML (booking form)     |
| POST   | `/client/cabin/<int:cabin_id>/book`        | Create booking         | Client        | `check_in`, `check_out`, `guests`, `observations`, `breakfast_included` | Redirect to bookings    |
| GET    | `/client/bookings`                         | List user's bookings   | Client        | N/A                                                       | HTML (bookings list)    |
| GET    | `/client/booking/<int:booking_id>`         | View booking details   | Client        | N/A                                                       | HTML (booking detail)   |
| POST   | `/client/booking/<int:booking_id>/cancel`  | Cancel booking         | Client        | N/A                                                       | Redirect to bookings    |
| POST   | `/client/booking/<int:booking_id>/review`  | Submit review          | Client        | `rating`, `comment`                                       | Redirect to bookings    |

---

### Service Interface Patterns

#### 1. Request-Response Pattern
```python
# Example: Create Booking Flow
Request:
  POST /client/cabin/5/book
  Headers: {Cookie: session_id=abc123, Content-Type: application/x-www-form-urlencoded}
  Body: check_in=2026-02-01&check_out=2026-02-05&guests=2&breakfast_included=on

Processing:
  1. Validate session → Extract user_id
  2. Validate form data → Parse dates, guests
  3. Business logic → Calculate nights, price, check availability
  4. Database → INSERT INTO bookings (...)
  5. Flash message → "Booking created successfully!"

Response:
  HTTP 302 Redirect
  Location: /client/bookings
  Set-Cookie: session_id=abc123 (updated)
```

#### 2. File Upload Pattern
```python
# Example: Add Cabin with Image
Request:
  POST /admin/cabin/add
  Headers: {Cookie: session_id=xyz789, Content-Type: multipart/form-data}
  Body: 
    - name: "Ocean View Suite"
    - cabin_number: "006"
    - capacity: 4
    - price_per_night: 300.00
    - image_file: [binary data, cabin.jpg]

Processing:
  1. Validate file extension → allowed_file()
  2. Secure filename → secure_filename("cabin_006_20260122_143022.jpg")
  3. Save to filesystem → static/uploads/cabin_006_20260122_143022.jpg
  4. Store path in DB → INSERT cabin with image_url='/static/uploads/...'

Response:
  HTTP 302 Redirect
  Location: /admin/cabins
  Flash: "Cabin added successfully"
```

#### 3. Session-Based Authentication
```python
# Authentication Flow
Login:
  POST /login → Validate credentials → Set session['user_id'] → Redirect

Protected Route:
  GET /client/bookings → @login_required → Check session['user_id']
    - If present: Execute route handler
    - If absent: Redirect to /login

Logout:
  GET /logout → session.clear() → Redirect to /login
```

---

## Client-Server Interaction

### Sequence Diagram: Complete Booking Flow

```
┌────────┐        ┌─────────┐        ┌──────────┐        ┌──────────┐
│ Client │        │  Flask  │        │ Business │        │ Database │
│Browser │        │ Server  │        │  Logic   │        │ (SQLite) │
└────┬───┘        └────┬────┘        └────┬─────┘        └────┬─────┘
     │                 │                  │                     │
     │ 1. HTTP GET     │                  │                     │
     │ /client/cabin/5/book               │                     │
     ├────────────────►│                  │                     │
     │                 │                  │                     │
     │                 │ 2. Fetch cabin data                    │
     │                 ├──────────────────┼────────────────────►│
     │                 │                  │  SELECT * FROM      │
     │                 │                  │  cabins WHERE id=5  │
     │                 │◄─────────────────┼─────────────────────┤
     │                 │                  │  {cabin data}       │
     │                 │                  │                     │
     │◄────────────────┤ 3. Render HTML   │                     │
     │  HTML Form      │  with cabin info │                     │
     │  (booking form) │                  │                     │
     │                 │                  │                     │
     │ 4. User fills   │                  │                     │
     │    form and     │                  │                     │
     │    submits      │                  │                     │
     │                 │                  │                     │
     │ 5. HTTP POST    │                  │                     │
     │ /client/cabin/5/book               │                     │
     │ Body: check_in=2026-02-01...       │                     │
     ├────────────────►│                  │                     │
     │                 │                  │                     │
     │                 │ 6. Extract & validate form data        │
     │                 ├─────────────────►│                     │
     │                 │                  │ • Parse dates       │
     │                 │                  │ • Calculate nights  │
     │                 │                  │ • Calculate price   │
     │                 │                  │                     │
     │                 │                  │ 7. Check availability│
     │                 │                  ├────────────────────►│
     │                 │                  │  SELECT COUNT(*)    │
     │                 │                  │  FROM bookings      │
     │                 │                  │  WHERE overlaps...  │
     │                 │                  │◄────────────────────┤
     │                 │                  │  count=0 (available)│
     │                 │                  │                     │
     │                 │                  │ 8. Create booking   │
     │                 │                  ├────────────────────►│
     │                 │                  │  INSERT INTO        │
     │                 │                  │  bookings (...)     │
     │                 │                  │◄────────────────────┤
     │                 │                  │  Success, ID=123    │
     │                 │◄─────────────────┤                     │
     │                 │ Success          │                     │
     │                 │                  │                     │
     │◄────────────────┤ 9. HTTP 302      │                     │
     │ Redirect to     │ Redirect +       │                     │
     │ /client/bookings│ flash message    │                     │
     │                 │                  │                     │
     │ 10. HTTP GET    │                  │                     │
     │ /client/bookings│                  │                     │
     ├────────────────►│                  │                     │
     │                 │                  │                     │
     │                 │ 11. Fetch user bookings                │
     │                 ├──────────────────┼────────────────────►│
     │                 │                  │  SELECT bookings... │
     │                 │◄─────────────────┼─────────────────────┤
     │                 │                  │  [booking list]     │
     │                 │                  │                     │
     │◄────────────────┤ 12. Render HTML  │                     │
     │  Bookings page  │  with flash      │                     │
     │  with success   │  message         │                     │
     │  message        │                  │                     │
     │                 │                  │                     │
```

### Request/Response Cycle Details

#### Phase 1: Initial Page Load
1. **Browser** sends GET request to view booking form
2. **Flask** routes request to `@app.route('/client/cabin/<int:cabin_id>/book')`
3. **Authentication Layer** checks session for `user_id` via `@login_required`
4. **Data Layer** queries cabin information from database
5. **Template Engine** (Jinja2) renders HTML with cabin data
6. **Browser** receives and displays form

#### Phase 2: Form Submission
1. **Browser** sends POST request with form data (check-in, check-out, guests)
2. **Flask** parses multipart/form-data
3. **Business Logic**:
   - Validates date format and logical consistency
   - Calculates derived values (nights, total price)
   - Queries database for conflicting bookings
   - Determines cabin availability
4. **Data Layer** executes INSERT statement if available
5. **Session Management** stores flash message for next request
6. **Flask** sends 302 redirect response

#### Phase 3: Confirmation Display
1. **Browser** follows redirect to bookings list page
2. **Flask** retrieves flash message from session
3. **Data Layer** queries user's bookings with JOIN to cabins
4. **Template Engine** renders bookings with flash message
5. **Browser** displays success confirmation

---

### Static File Serving

```
Client Request: GET /static/uploads/cabin_001_20260122.jpg
                              │
                              ▼
         ┌────────────────────────────────┐
         │  Flask Static File Handler     │
         │  (Werkzeug FileSystemLoader)   │
         └────────────┬───────────────────┘
                      │
                      ▼
         ┌────────────────────────────────┐
         │  Filesystem (OS)               │
         │  Path: static/uploads/...      │
         └────────────┬───────────────────┘
                      │
                      ▼
         ┌────────────────────────────────┐
         │  Response                      │
         │  Content-Type: image/jpeg      │
         │  Body: [binary image data]     │
         └────────────────────────────────┘
```

---

## Reliability, Fault Tolerance & Scalability

### 1. Reliability Analysis

#### Current Implementation

**Strengths:**
- ✅ **ACID Transactions**: SQLite provides atomicity, consistency, isolation, durability
- ✅ **Password Security**: Werkzeug hashing prevents plaintext password storage
- ✅ **Session Management**: Secure session tokens prevent unauthorized access
- ✅ **Input Validation**: Form validation prevents invalid data entry
- ✅ **Conflict Prevention**: Availability check prevents double-booking

**Current Limitations:**
- ⚠️ **Single Point of Failure**: One server, one database file
- ⚠️ **No Data Replication**: Database loss = total data loss
- ⚠️ **Limited Concurrency**: SQLite write locks can cause contention
- ⚠️ **No Health Monitoring**: No alerting for failures
- ⚠️ **Synchronous Operations**: Blocking I/O can delay responses

---

### 2. Fault Tolerance Strategies

#### Current State
- **Database Crashes**: No automatic recovery, requires manual restart
- **File System Errors**: Image upload failures display generic errors
- **Network Failures**: No retry mechanism for external resources
- **Session Loss**: Users logged out if session storage corrupted

#### Recommended Improvements

```
┌─────────────────────────────────────────────────────────────────┐
│             FAULT TOLERANCE ARCHITECTURE (PROPOSED)              │
└─────────────────────────────────────────────────────────────────┘

┌───────────────────────────────────────────────────────────────┐
│  LAYER 1: Application Redundancy                              │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐        │
│  │  Flask App   │  │  Flask App   │  │  Flask App   │        │
│  │  Instance 1  │  │  Instance 2  │  │  Instance 3  │        │
│  └──────┬───────┘  └──────┬───────┘  └──────┬───────┘        │
│         └──────────────────┼──────────────────┘                │
│                            │                                   │
└────────────────────────────┼───────────────────────────────────┘
                             │
                             ▼
┌───────────────────────────────────────────────────────────────┐
│  LAYER 2: Load Balancer (Nginx/HAProxy)                      │
│  • Health Checks: Ping /health every 10s                      │
│  • Failover: Route to healthy instances                       │
│  • Session Affinity: Sticky sessions or shared session store  │
└────────────────────────────┬──────────────────────────────────┘
                             │
                             ▼
┌───────────────────────────────────────────────────────────────┐
│  LAYER 3: Database Resilience                                 │
│  ┌─────────────────┐         ┌─────────────────┐             │
│  │  Primary DB     │────────►│  Replica DB     │             │
│  │  (PostgreSQL)   │  Async  │  (Read-only)    │             │
│  │  Write Ops      │  Repl.  │  Read Ops       │             │
│  └─────────────────┘         └─────────────────┘             │
│          │                                                     │
│          ▼                                                     │
│  ┌─────────────────┐                                          │
│  │  WAL Archive    │  (Point-in-time recovery)                │
│  │  Backups (S3)   │                                          │
│  └─────────────────┘                                          │
└───────────────────────────────────────────────────────────────┘
                             │
                             ▼
┌───────────────────────────────────────────────────────────────┐
│  LAYER 4: File Storage Resilience                             │
│  ┌─────────────────┐         ┌─────────────────┐             │
│  │  S3/Object      │────────►│  CDN (CloudFront│             │
│  │  Storage        │         │  or Cloudflare) │             │
│  │  (Primary)      │         │  (Edge Cache)   │             │
│  └─────────────────┘         └─────────────────┘             │
│  • Multi-region replication                                   │
│  • 99.999999999% durability (11 nines)                        │
└───────────────────────────────────────────────────────────────┘
```

#### Fault Handling Matrix

| Failure Type          | Detection Method       | Recovery Strategy              | Expected Downtime |
|-----------------------|------------------------|--------------------------------|-------------------|
| App Server Crash      | Health check failure   | Load balancer routes to backup | < 10 seconds      |
| Database Crash        | Connection timeout     | Failover to replica            | < 30 seconds      |
| Disk Full             | Storage monitoring     | Auto-scale storage / alerting  | Manual intervention|
| Network Partition     | Request timeout        | Retry with exponential backoff | Transparent       |
| Image Upload Failure  | Exception handler      | Rollback transaction, retry    | User re-submits   |
| Session Store Loss    | Redis cluster failure  | Use backup Redis node          | < 5 seconds       |

---

### 3. Scalability Analysis

#### Current Bottlenecks

1. **Database Write Locks** (SQLite Limitation)
   - SQLite allows only one writer at a time
   - Impact: Concurrent bookings can cause delays
   - Solution: Migrate to PostgreSQL/MySQL with connection pooling

2. **Single-Server Architecture**
   - CPU/Memory limited to one machine
   - Impact: Cannot handle traffic spikes
   - Solution: Horizontal scaling with multiple app instances

3. **Local File Storage**
   - Disk space limited to server capacity
   - Impact: Cannot share images across multiple servers
   - Solution: Object storage (S3) with CDN

4. **No Caching Layer**
   - Every request hits database
   - Impact: Slow response for frequently accessed data
   - Solution: Redis caching for cabin listings, availability

#### Scalability Roadmap

```
┌─────────────────────────────────────────────────────────────────┐
│            SCALABILITY ARCHITECTURE (TARGET STATE)               │
└─────────────────────────────────────────────────────────────────┘

                          ┌─────────────┐
                          │   Client    │
                          │   Browsers  │
                          └──────┬──────┘
                                 │
                                 ▼
              ┌───────────────────────────────────┐
              │  CDN (CloudFront / Cloudflare)   │
              │  • Static Assets (CSS, JS)        │
              │  • Cached Images                  │
              └───────────────┬───────────────────┘
                              │
                              ▼
              ┌───────────────────────────────────┐
              │  Load Balancer (Nginx)            │
              │  • SSL Termination                │
              │  • Rate Limiting (DDoS protection)│
              │  • Sticky Sessions                │
              └───────────────┬───────────────────┘
                              │
                ┌─────────────┼─────────────┐
                │             │             │
                ▼             ▼             ▼
        ┌──────────┐  ┌──────────┐  ┌──────────┐
        │ Flask-1  │  │ Flask-2  │  │ Flask-N  │  (Horizontal Scaling)
        │ App      │  │ App      │  │ App      │
        │ Container│  │ Container│  │ Container│  Auto-scale: 3-20 instances
        └────┬─────┘  └────┬─────┘  └────┬─────┘
             │             │             │
             └─────────────┼─────────────┘
                           │
          ┌────────────────┼────────────────┐
          │                │                │
          ▼                ▼                ▼
  ┌───────────────┐ ┌───────────────┐ ┌───────────────┐
  │ Redis Cluster │ │  PostgreSQL   │ │  S3 Storage   │
  │ (Cache Layer) │ │  (Primary DB) │ │  (Images)     │
  │               │ │               │ │               │
  │ • Sessions    │ │ • Read/Write  │ │ • Multi-AZ    │
  │ • Cabin List  │ │ • Connection  │ │ • Versioning  │
  │ • Availability│ │   Pooling     │ │ • Lifecycle   │
  └───────────────┘ │ • Replication │ │   Policies    │
                    │               │ └───────────────┘
                    ├───────────────┤
                    │  Read Replica │
                    │  (PostgreSQL) │
                    └───────────────┘

  ┌───────────────────────────────────────────────────────────────┐
  │  MONITORING & OBSERVABILITY                                   │
  │  • Application Metrics: Prometheus                            │
  │  • Logging: ELK Stack (Elasticsearch, Logstash, Kibana)       │
  │  • Tracing: Jaeger (distributed tracing)                      │
  │  • Alerting: PagerDuty / Slack integration                    │
  └───────────────────────────────────────────────────────────────┘
```

#### Scaling Strategies

**Vertical Scaling (Short-term)**
- ✅ Increase server CPU: 2 cores → 8 cores
- ✅ Increase RAM: 2GB → 16GB
- ✅ Upgrade to PostgreSQL with connection pooling
- **Capacity**: 100 → 500 concurrent users

**Horizontal Scaling (Medium-term)**
- ✅ Deploy 3-5 app instances behind load balancer
- ✅ Implement Redis for session storage (shared state)
- ✅ Add read replicas for database queries
- **Capacity**: 500 → 5,000 concurrent users

**Microservices (Long-term)**
- ✅ Split into services: Auth, Booking, Cabin, Review
- ✅ Message queue (RabbitMQ) for async processing
- ✅ Event-driven architecture for real-time updates
- **Capacity**: 5,000 → 50,000+ concurrent users

---

### 4. Performance Optimization

#### Database Optimization

```sql
-- Add indexes for common queries
CREATE INDEX idx_bookings_cabin_dates 
  ON bookings(cabin_id, check_in, check_out, status);

CREATE INDEX idx_bookings_user 
  ON bookings(user_id, status);

CREATE INDEX idx_reviews_cabin 
  ON reviews(cabin_id, created_at DESC);

-- Connection pooling (PostgreSQL)
from sqlalchemy import create_engine
from sqlalchemy.pool import QueuePool

engine = create_engine(
    'postgresql://user:pass@localhost/rentbnb',
    poolclass=QueuePool,
    pool_size=20,
    max_overflow=40,
    pool_recycle=3600
)
```

#### Caching Strategy

```python
# Redis caching for cabin listings
import redis
import json

cache = redis.Redis(host='localhost', port=6379, db=0)

def get_cabins():
    # Try cache first
    cached = cache.get('cabins:all')
    if cached:
        return json.loads(cached)
    
    # Cache miss - query database
    db = get_db()
    cabins = db.execute('SELECT * FROM cabins').fetchall()
    
    # Store in cache for 15 minutes
    cache.setex('cabins:all', 900, json.dumps(cabins))
    
    return cabins

# Invalidate cache on cabin update
def update_cabin(cabin_id, data):
    db = get_db()
    db.execute('UPDATE cabins SET ... WHERE id = ?', ...)
    db.commit()
    
    # Invalidate cache
    cache.delete('cabins:all')
    cache.delete(f'cabin:{cabin_id}')
```

#### Asynchronous Processing

```python
# Background task queue for email notifications
from celery import Celery

app_celery = Celery('rentbnb', broker='redis://localhost:6379/0')

@app_celery.task
def send_booking_confirmation(booking_id):
    # Fetch booking details
    db = get_db()
    booking = db.execute('SELECT * FROM bookings WHERE id = ?', (booking_id,)).fetchone()
    
    # Send email (non-blocking)
    send_email(
        to=booking['guest_email'],
        subject='Booking Confirmation',
        body=f'Your booking #{booking_id} is confirmed!'
    )

# In route handler
@app.route('/client/cabin/<int:cabin_id>/book', methods=['POST'])
def book_cabin(cabin_id):
    # ... create booking ...
    db.execute('INSERT INTO bookings (...) VALUES (...)')
    booking_id = db.lastrowid
    db.commit()
    
    # Async email sending (doesn't block response)
    send_booking_confirmation.delay(booking_id)
    
    return redirect(url_for('client_bookings'))
```

---

## Security Considerations

### Current Security Measures

1. **Authentication**
   - Password hashing using Werkzeug (scrypt algorithm)
   - Session-based authentication with secure cookies
   - Role-based access control (client vs admin)

2. **Input Validation**
   - Form data sanitization
   - File upload validation (extension, size)
   - SQL parameterization (prevents SQL injection)

3. **Authorization**
   - `@login_required` decorator for protected routes
   - `@admin_required` decorator for admin functions
   - User ownership verification for bookings

### Security Enhancements Needed

```python
# 1. HTTPS Enforcement
from flask_talisman import Talisman
Talisman(app, force_https=True)

# 2. CSRF Protection
from flask_wtf.csrf import CSRFProtect
csrf = CSRFProtect(app)

# 3. Rate Limiting
from flask_limiter import Limiter
limiter = Limiter(app, key_func=get_remote_address)

@app.route('/login', methods=['POST'])
@limiter.limit("5 per minute")  # Prevent brute force
def login():
    ...

# 4. Security Headers
@app.after_request
def set_security_headers(response):
    response.headers['X-Content-Type-Options'] = 'nosniff'
    response.headers['X-Frame-Options'] = 'DENY'
    response.headers['X-XSS-Protection'] = '1; mode=block'
    return response

# 5. File Upload Security
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif', 'webp'}
MAX_FILE_SIZE = 5 * 1024 * 1024  # 5MB

def validate_file_content(file):
    # Verify file type using python-magic (not just extension)
    import magic
    mime = magic.from_buffer(file.read(1024), mime=True)
    file.seek(0)
    return mime in ['image/png', 'image/jpeg', 'image/gif', 'image/webp']
```

---

## Future Enhancements

### Phase 1: Core Improvements (3 months)
- [ ] Migrate to PostgreSQL
- [ ] Implement Redis caching
- [ ] Add email notifications (Celery)
- [ ] Deploy to cloud (AWS/Azure/GCP)
- [ ] Set up CI/CD pipeline

### Phase 2: Feature Expansion (6 months)
- [ ] Payment gateway integration (Stripe)
- [ ] Real-time availability calendar
- [ ] Guest review system
- [ ] Admin analytics dashboard
- [ ] Mobile-responsive redesign

### Phase 3: Advanced Features (12 months)
- [ ] Microservices architecture
- [ ] GraphQL API
- [ ] WebSocket for real-time updates
- [ ] Machine learning for pricing optimization
- [ ] Multi-language support

---

## Conclusion

The RentBnb system currently implements a solid **monolithic layered architecture** suitable for development and small-scale deployment. The design prioritizes:

- **Simplicity**: Clear separation of concerns across presentation, business logic, and data layers
- **Security**: Password hashing, session management, role-based access
- **Functionality**: Complete booking workflow with admin management

To achieve production-grade **reliability, fault tolerance, and scalability**, the system requires:

1. **Infrastructure upgrades**: PostgreSQL, Redis, load balancers
2. **Architectural patterns**: Caching, async processing, connection pooling
3. **Operational tooling**: Monitoring, logging, automated backups
4. **Security hardening**: HTTPS, CSRF protection, rate limiting

This document serves as a blueprint for evolving the system from a development prototype to an enterprise-ready application capable of handling thousands of concurrent users with 99.9% uptime.

---

**Document Version**: 1.0  
**Last Updated**: January 22, 2026  
**Author**: System Design Team  
**Status**: Approved for Implementation
