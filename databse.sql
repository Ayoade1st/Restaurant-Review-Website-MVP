CREATE TABLE User (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  username VARCHAR(50) NOT NULL UNIQUE,
  password TEXT NOT NULL,
  email VARCHAR(254) NOT NULL UNIQUE,
  created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
  last_login_at DATETIME,
  is_active BOOLEAN DEFAULT TRUE,
  role VARCHAR(20) DEFAULT 'user',
  profile_image_url TEXT,
  first_name VARCHAR(50),
  last_name VARCHAR(50),
  bio TEXT
);

CREATE TABLE Restaurant (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  name VARCHAR(100) NOT NULL,
  street_address VARCHAR(255),
  city VARCHAR(100),
  state VARCHAR(100),
  zip_code VARCHAR(20),
  country VARCHAR(100),
  phone_number VARCHAR(15),
  email VARCHAR(254),
  website_url TEXT,
  cuisine_type VARCHAR(50),
  operating_hours TEXT,
  rating_average DECIMAL(3,2),
  review_count INTEGER DEFAULT 0,
  menu TEXT,
  owner_id INTEGER,
  created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
  updated_at DATETIME DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE Review (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  user_id INTEGER NOT NULL,
  restaurant_id INTEGER NOT NULL,
  rating DECIMAL(2,1) NOT NULL,
  title VARCHAR(100),
  review_text TEXT,
  date_posted DATETIME DEFAULT CURRENT_TIMESTAMP,
  likes INTEGER DEFAULT 0,
  status VARCHAR(20) DEFAULT 'approved',
  helpful_count INTEGER DEFAULT 0,
  FOREIGN KEY (user_id) REFERENCES User(id),
  FOREIGN KEY (restaurant_id) REFERENCES Restaurant(id)
);

CREATE TABLE Rating (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  user_id INTEGER NOT NULL,
  restaurant_id INTEGER NOT NULL,
  rating_value INTEGER NOT NULL,
  comment TEXT,
  date_created DATETIME DEFAULT CURRENT_TIMESTAMP,
  ip_address VARCHAR(45),
  FOREIGN KEY (user_id) REFERENCES User(id),
  FOREIGN KEY (restaurant_id) REFERENCES Restaurant(id)
);