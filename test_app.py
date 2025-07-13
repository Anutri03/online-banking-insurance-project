#!/usr/bin/env python3
"""
Simple test script to verify the application components work correctly.
"""

import sys
import os

def test_imports():
    """Test that all modules can be imported successfully."""
    print("Testing imports...")
    
    try:
        from app import create_app
        print("✓ app.py imported successfully")
    except Exception as e:
        print(f"✗ Failed to import app.py: {e}")
        return False
    
    try:
        from models import db, User, BankAccount, Transaction, InsurancePolicy, InsuranceClaim
        print("✓ models.py imported successfully")
    except Exception as e:
        print(f"✗ Failed to import models.py: {e}")
        return False
    
    try:
        from forms import LoginForm, RegisterForm, TransactionForm, InsurancePolicyForm, ClaimForm, AccountForm
        print("✓ forms.py imported successfully")
    except Exception as e:
        print(f"✗ Failed to import forms.py: {e}")
        return False
    
    try:
        from routes import routes_bp
        print("✓ routes.py imported successfully")
    except Exception as e:
        print(f"✗ Failed to import routes.py: {e}")
        return False
    
    try:
        from admin import admin_bp
        print("✓ admin.py imported successfully")
    except Exception as e:
        print(f"✗ Failed to import admin.py: {e}")
        return False
    
    try:
        from config import config
        print("✓ config.py imported successfully")
    except Exception as e:
        print(f"✗ Failed to import config.py: {e}")
        return False
    
    return True

def test_app_creation():
    """Test that the Flask app can be created successfully."""
    print("\nTesting app creation...")
    
    try:
        from app import create_app
        from models import db
        
        # Test development config
        app = create_app('development')
        print("✓ Development app created successfully")
        
        # Test testing config
        app = create_app('testing')
        print("✓ Testing app created successfully")
        
        # Test production config
        app = create_app('production')
        print("✓ Production app created successfully")
        
        return True
    except Exception as e:
        print(f"✗ Failed to create app: {e}")
        return False

def test_database_models():
    """Test that database models can be created."""
    print("\nTesting database models...")
    
    try:
        from app import create_app
        from models import db, User, BankAccount, Transaction, InsurancePolicy, InsuranceClaim
        
        app = create_app('testing')
        
        with app.app_context():
            # Create tables
            db.create_all()
            print("✓ Database tables created successfully")
            
            # Test model creation
            user = User(
                username='testuser',
                email='test@example.com',
                password_hash='test_hash',
                first_name='Test',
                last_name='User'
            )
            print("✓ User model created successfully")
            
            account = BankAccount(
                account_number='TEST123',
                account_type='savings',
                balance=1000.0,
                user_id=1
            )
            print("✓ BankAccount model created successfully")
            
            transaction = Transaction(
                transaction_id='TXN123',
                transaction_type='deposit',
                amount=100.0,
                account_id=1
            )
            print("✓ Transaction model created successfully")
            
            policy = InsurancePolicy(
                policy_number='POL123',
                policy_type='life',
                coverage_amount=50000.0,
                premium_amount=100.0,
                start_date='2024-01-01',
                end_date='2025-01-01',
                user_id=1
            )
            print("✓ InsurancePolicy model created successfully")
            
            claim = InsuranceClaim(
                claim_number='CLM123',
                policy_id=1,
                claim_amount=5000.0,
                description='Test claim'
            )
            print("✓ InsuranceClaim model created successfully")
            
            # Clean up
            db.drop_all()
            print("✓ Database cleaned up successfully")
            
        return True
    except Exception as e:
        print(f"✗ Failed to test database models: {e}")
        return False

def test_forms():
    """Test that forms can be created and validated."""
    print("\nTesting forms...")
    
    try:
        from app import create_app
        from forms import LoginForm, RegisterForm, TransactionForm, InsurancePolicyForm, ClaimForm, AccountForm
        
        app = create_app('testing')
        
        with app.app_context():
            # Test form creation
            login_form = LoginForm()
            register_form = RegisterForm()
            transaction_form = TransactionForm()
            policy_form = InsurancePolicyForm()
            claim_form = ClaimForm()
            account_form = AccountForm()
            
            print("✓ All forms created successfully")
            
            # Test basic form validation
            if login_form.validate_on_submit() is False:  # Should be False when no data
                print("✓ Form validation working correctly")
            
        return True
    except Exception as e:
        print(f"✗ Failed to test forms: {e}")
        return False

def main():
    """Run all tests."""
    print("Running application tests...\n")
    
    tests = [
        test_imports,
        test_app_creation,
        test_database_models,
        test_forms
    ]
    
    passed = 0
    total = len(tests)
    
    for test in tests:
        if test():
            passed += 1
        print()
    
    print(f"Tests completed: {passed}/{total} passed")
    
    if passed == total:
        print("🎉 All tests passed! The application is ready to run.")
        return 0
    else:
        print("❌ Some tests failed. Please check the errors above.")
        return 1

if __name__ == '__main__':
    sys.exit(main()) 