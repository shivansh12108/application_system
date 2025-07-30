# application_system
# Application Management System

## Overview
A web-based application management system built with Flask and MySQL that allows applicants to submit their applications and administrators to manage them. The system features a secure admin panel, file upload capabilities, and a user-friendly interface.

## Features
- **Applicant Portal**
  - User registration with resume upload (PDF)
  - Profile information submission
  - Professional links (GitHub, LinkedIn)
  - Mobile number verification

- **Admin Dashboard**
  - Secure login system
  - View all applications
  - Create, edit, and delete applications
  - Access uploaded resumes
  - View applicant contact information and professional profiles

## Technologies Used
- Backend: Python Flask
- Database: MySQL
- Frontend: HTML, CSS, JavaScript
- Security: Session-based authentication

## Setup Instructions
1. Install required Python packages:
   ```bash
   pip install flask flask-mysqldb
   ```

2. Set up MySQL database:
   - Create a database named 'application_form_db'
   - Import the provided `db.sql` file

3. Configure MySQL connection in `app.py`:
   ```python
   app.config['MYSQL_HOST'] = 'localhost'
   app.config['MYSQL_USER'] = 'root'
   app.config['MYSQL_PASSWORD'] = ''
   app.config['MYSQL_DB'] = 'application_form_db'
   ```

4. Run the application:
   ```bash
   python app.py
   ```

5. Access the application:
   - Main application: http://localhost:5000
   - Admin login: http://localhost:5000/admin/login

## Default Admin Credentials
- Email: admin@example.com
- Password: adminpass

## Project Structure
```
├── app.py              # Main application file
├── db.sql              # Database schema and initial data
├── templates/          # HTML templates
│   ├── form.html           # Application form
│   ├── admin_login.html    # Admin login page
│   ├── admin_dashboard.html# Admin dashboard
│   └── admin_form.html     # Admin edit form
└── uploads/           # Directory for uploaded resumes
```

## Security Features
- Password protection for admin access
- Session-based authentication
- Protected admin routes
- Secure file upload handling

## License
This project is licensed under the MIT License - see the LICENSE file for details.
