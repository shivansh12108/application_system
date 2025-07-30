CREATE DATABASE IF NOT EXISTS application_form_db;
USE application_form_db;

CREATE TABLE IF NOT EXISTS applicants (
    id INT AUTO_INCREMENT PRIMARY KEY,
    first_name VARCHAR(100),
    last_name VARCHAR(100),
    dob DATE,
    gender VARCHAR(10),
    age INT,
    email VARCHAR(150),
    position VARCHAR(50),
    languages VARCHAR(150),
    password VARCHAR(150),
    mobile VARCHAR(20),
    github VARCHAR(200),
    linkedin VARCHAR(200),
    resume VARCHAR(255)
);

CREATE TABLE IF NOT EXISTS admins (
    id INT AUTO_INCREMENT PRIMARY KEY,
    email VARCHAR(150) UNIQUE,
    password VARCHAR(150)
);

-- Insert a default admin (use a secure password in production)
INSERT IGNORE INTO admins (email, password) VALUES ('admin@example.com', 'adminpass');
