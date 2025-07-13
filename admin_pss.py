from app import create_app, db, User
from werkzeug.security import generate_password_hash
from config import config

# Create app context with development config
app = create_app('development')

with app.app_context():
    # Create database tables
    db.create_all()
    
    # Check if admin user exists
    admin_user = User.query.filter_by(username='admin').first()
    
    if admin_user:
        # Update admin password
        admin_user.password_hash = generate_password_hash('admin123')
        db.session.commit()
        print("Admin password updated successfully!")
        print("Username: admin")
        print("Password: admin123")
    else:
        # Create admin user
        admin_user = User(
            username='admin',
            email='admin@digitalbank.com',
            password_hash=generate_password_hash('admin123'),
            first_name='Admin',
            last_name='User',
            phone='123-456-7890',
            is_active=True
        )
        db.session.add(admin_user)
        db.session.commit()
        print("Admin user created successfully!")
        print("Username: admin")
        print("Password: admin123")
    
    print("\nYou can now login with these credentials.")
    print("IMPORTANT: Change the admin password after first login!")