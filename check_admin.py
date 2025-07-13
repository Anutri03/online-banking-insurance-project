"""
Script to check admin user status and help troubleshoot login issues.
"""

from app import create_app
from models import db, User

def check_admin_user():
    """Check if admin user exists and is properly configured."""
    print(" Checking Admin User Status...")
    print("-" * 50)
    
    app = create_app('development')
    
    with app.app_context():
        # Check if database exists
        try:
            db.create_all()
            print("Database tables created/verified")
        except Exception as e:
            print(f"Database error: {e}")
            return
        
        # Check for admin user
        admin_user = User.query.filter_by(username='admin').first()
        
        if admin_user:
            print("    Admin user found!")
            print(f"   Username: {admin_user.username}")
            print(f"   Email: {admin_user.email}")
            print(f"   First Name: {admin_user.first_name}")
            print(f"   Last Name: {admin_user.last_name}")
            print(f"   Is Active: {admin_user.is_active}")
            print(f"   Created: {admin_user.created_at}")
            print()
            print("   Login Credentials:")
            print("   Email: admin@digitalbank.com")
            print("   Password: admin123")
            print()
            print("   To access admin panel:")
            print("   1. Go to: http://localhost:5000")
            print("   2. Click 'Login as Admin' button")
            print("   3. Click 'Login' button")
            print("   4. Look for 'Admin' dropdown in navigation")
            print()
            
            # Check total users
            total_users = User.query.count()
            print(f"Total users in system: {total_users}")
            
        else:
            print("Admin user not found!")
            print()
            print("To create admin user, run:")
            print("   python admin_pss.py")
            print()
            print("Then try logging in again.")

def main():
    """Main function."""
    try:
        check_admin_user()
    except Exception as e:
        print(f" Error: {e}")
        print()
        print(" Try running:")
        print("   python admin_pss.py")
        print("   python run.py")

if __name__ == '__main__':
    main() 