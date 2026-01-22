-- Users table
CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    email TEXT UNIQUE NOT NULL,
    password TEXT NOT NULL,
    phone TEXT,
    national_id TEXT,
    role TEXT NOT NULL DEFAULT 'client', -- 'client' or 'admin'
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Cabins/Properties table
CREATE TABLE IF NOT EXISTS cabins (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    cabin_number TEXT UNIQUE NOT NULL,
    capacity INTEGER NOT NULL,
    price_per_night REAL NOT NULL,
    description TEXT,
    amenities TEXT,
    image_url TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Bookings table
CREATE TABLE IF NOT EXISTS bookings (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER NOT NULL,
    cabin_id INTEGER NOT NULL,
    check_in DATE NOT NULL,
    check_out DATE NOT NULL,
    num_nights INTEGER NOT NULL,
    num_guests INTEGER NOT NULL,
    observations TEXT,
    breakfast_included BOOLEAN DEFAULT 0,
    total_price REAL NOT NULL,
    status TEXT NOT NULL DEFAULT 'unconfirmed', -- 'unconfirmed', 'checked_in', 'checked_out', 'cancelled'
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users (id),
    FOREIGN KEY (cabin_id) REFERENCES cabins (id)
);

-- Reviews table
CREATE TABLE IF NOT EXISTS reviews (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER NOT NULL,
    cabin_id INTEGER NOT NULL,
    booking_id INTEGER NOT NULL,
    rating INTEGER NOT NULL CHECK(rating >= 1 AND rating <= 5),
    comment TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users (id),
    FOREIGN KEY (cabin_id) REFERENCES cabins (id),
    FOREIGN KEY (booking_id) REFERENCES bookings (id)
);

INSERT OR IGNORE INTO users (id, name, email, password, role) 
VALUES (1, 'Admin User', 'admin@wildoasis.com', 'scrypt:32768:8:1$Z8QJxYGxMJQXqFRm$c7a8e6d7f0b5e4c9d8a3f2e1b6c5d4a3e2f1b0c9d8e7f6a5b4c3d2e1f0a9b8c7d6e5f4a3b2c1d0e9f8a7b6c5d4e3f2a1', 'admin');

-- Insert sample cabins
INSERT OR IGNORE INTO cabins (name, cabin_number, capacity, price_per_night, description, amenities, image_url) 
VALUES 
    ('Mountain View Cabin', '001', 4, 250.00, 'Beautiful cabin with stunning mountain views', 'WiFi, Kitchen, Fireplace, Hot Tub', 'https://images.unsplash.com/photo-1587061949409-02df41d5e562?w=500'),
    ('Lakeside Retreat', '002', 6, 350.00, 'Spacious cabin right by the lake', 'WiFi, Kitchen, BBQ, Boat Dock', 'https://images.unsplash.com/photo-1449158743715-0a90ebb6d2d8?w=500'),
    ('Forest Haven', '003', 2, 180.00, 'Cozy cabin nestled in the forest', 'WiFi, Fireplace, Hiking Trails', 'https://images.unsplash.com/photo-1510798831971-661eb04b3739?w=500'),
    ('Riverside Lodge', '004', 8, 450.00, 'Large lodge perfect for groups', 'WiFi, Kitchen, Game Room, Fire Pit', 'https://images.unsplash.com/photo-1518732714860-b62714ce0c59?w=500'),
    ('Sunset Cabin', '005', 3, 200.00, 'Watch beautiful sunsets from your porch', 'WiFi, Kitchen, Deck, Hammock', 'https://images.unsplash.com/photo-1464207687429-7505649dae38?w=500');

INSERT OR IGNORE INTO users (id, name, email, password, phone, national_id, role) 
VALUES (2, 'Tomioka Giyu', 'test@gmail.com', 'scrypt:32768:8:1$uNXqHRzGvKpYmQZl$a8b7c6d5e4f3a2b1c0d9e8f7a6b5c4d3e2f1a0b9c8d7e6f5a4b3c2d1e0f9a8b7c6d5e4f3a2b1c0d9e8f7a6b5c4d3e2f1', '+1234567890', '3525435345', 'client');
