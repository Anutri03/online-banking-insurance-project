#!/usr/bin/env python3
"""
Simple script to run the DigitalBank application.
"""

import os
from app import create_app
from models import db

def main():
    """Run the application."""
    print("🚀 Starting DigitalBank Application...")
    
    # Create the application
    app = create_app()
    
    # Create database tables if they don't exist
    with app.app_context():
        db.create_all()
        print("✅ Database initialized")
    
    print("🌐 Application is running at: http://localhost:5000")
    print("📧 Admin login: admin@digitalbank.com / admin123")
    print("⏹️  Press Ctrl+C to stop the application")
    print("-" * 50)
    
    # Run the application
    app.run(debug=True, host='0.0.0.0', port=5000)

if __name__ == '__main__':
    main() 