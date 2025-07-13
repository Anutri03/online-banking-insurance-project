# Online Banking & Insurance System

An advanced web application for online banking and insurance management built with Python, Flask, and SQLAlchemy.

## Features

### Banking Features
- User account creation and management
- Multiple account types (checking, savings, business)
- Deposits, withdrawals, and transfers between accounts
- Transaction history with filtering and sorting
- Account statements and reports
- Real-time balance updates

### Insurance Features
- Multiple insurance policy types (health, auto, home, life)
- Policy management and renewal
- Premium payments
- Claims filing and tracking
- Policy documents and certificates

### General Features
- Secure user authentication and authorization
- Email notifications for important events
- User profile management
- Admin dashboard for system management
- RESTful API for third-party integrations
- Responsive web interface
- Form validation and error handling
- CSRF protection

## Technology Stack

- **Backend**: Python, Flask
- **Database**: SQLAlchemy ORM with SQLite/PostgreSQL
- **Authentication**: Flask-Login, JWT for API
- **Forms**: Flask-WTF, WTForms
- **Migrations**: Flask-Migrate, Alembic
- **Email**: Flask-Mail
- **Frontend**: HTML, CSS, JavaScript, Bootstrap
- **API**: RESTful API with JSON responses

## Installation

1. Clone the repository:
```bash
git clone https://github.com/yourusername/online-banking-insurance.git
cd online-banking-insurance
```

2. Create and activate a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Set up environment variables (optional):
```bash
# Create a .env file with your configuration
export FLASK_ENV=development
export SECRET_KEY=your-super-secret-key-change-this-in-production
export DATABASE_URL=sqlite:///site.db
```

5. Initialize the database and create admin user:
```bash
python admin_pss.py
```

6. Run the application:
```bash
python app.py
# or
flask run
```

## Configuration

The application uses a configuration system that supports different environments:

- **Development**: Default configuration for development
- **Production**: Secure configuration for production deployment
- **Testing**: Configuration for running tests

Key configuration options:
- `SECRET_KEY`: Flask secret key for session management
- `DATABASE_URL`: Database connection string
- `MAIL_SERVER`: SMTP server for email notifications
- `ADMIN_EMAIL`: Admin user email
- `ADMIN_PASSWORD`: Admin user password

## Project Structure

```
online-banking-insurance/
├── app.py                 # Application factory
├── config.py              # Configuration settings
├── models.py              # Database models
├── forms.py               # WTForms classes
├── routes.py              # Main route handlers
├── admin.py               # Admin route handlers
├── admin_pss.py           # Admin user setup script
├── requirements.txt       # Python dependencies
├── static/                # Static assets
│   ├── css/
│   ├── js/
│   └── img/
├── templates/             # Jinja2 templates
│   ├── admin/            # Admin templates
│   └── ...               # Other templates
└── instance/             # Instance-specific files
    └── site.db           # SQLite database
```

## API Documentation

The system provides a RESTful API for integration with other systems. API endpoints include:

- `/api/account_balance/<account_id>` - Get account balance
- `/admin/api/stats` - Get system statistics (admin only)

All API requests (except authentication) require a valid session.

## Security Features

- **CSRF Protection**: All forms are protected against CSRF attacks
- **Input Validation**: Comprehensive form validation using WTForms
- **SQL Injection Protection**: SQLAlchemy ORM prevents SQL injection
- **Session Security**: Secure session configuration
- **Password Hashing**: Passwords are hashed using Werkzeug
- **Access Control**: Role-based access control for admin functions

## Development

1. Install development dependencies:
```bash
pip install -r requirements.txt
```

2. Run tests (when implemented):
```bash
pytest
```

3. Check code style:
```bash
flake8
```

## Admin Access

After running `python admin_pss.py`, you can access the admin panel with:
- **Username**: admin
- **Password**: admin123

**Important**: Change the admin password after first login!

## Database Models

The application includes the following models:
- **User**: User accounts and profiles
- **BankAccount**: Bank accounts with balances
- **Transaction**: Financial transactions
- **InsurancePolicy**: Insurance policies
- **InsuranceClaim**: Insurance claims

## Error Handling

The application includes comprehensive error handling:
- Form validation errors
- Database operation errors
- Authentication errors
- Authorization errors
- General exception handling

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Contributors

- Your Name <your.email@example.com>

## Acknowledgments

- Flask and SQLAlchemy documentation
- Python community
- Open source contributors 