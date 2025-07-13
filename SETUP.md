# Quick Setup Guide

## 🚀 Quick Start

### 1. Install Dependencies
```bash
pip install -r requirements.txt
```

### 2. Set Up Admin User
```bash
python admin_pss.py
```

### 3. Run the Application
```bash
python run.py
```

### 4. Access the Application
- **Main Application**: http://localhost:5000
- **Admin Login**: admin@digitalbank.com / admin123

## 🔐 Admin Access

### Method 1: Use the Admin Login Button
1. Go to the login page
2. Click "Login as Admin" button
3. Click "Login" to access admin panel

### Method 2: Manual Login
1. Go to the login page
2. Enter: admin@digitalbank.com
3. Enter: admin123
4. Click "Login"

## 📋 Available Features

### For Regular Users
- ✅ User registration and login
- ✅ Create bank accounts (savings, checking, business)
- ✅ Make deposits and withdrawals
- ✅ View transaction history
- ✅ Create insurance policies
- ✅ Submit insurance claims

### For Admin Users
- ✅ View all users and accounts
- ✅ Manage user accounts
- ✅ View all transactions
- ✅ Process insurance claims
- ✅ System analytics and reports
- ✅ Export data to CSV

## 🔧 Configuration

The application uses environment variables for configuration:

```bash
# Optional: Set environment variables
export FLASK_ENV=development
export SECRET_KEY=your-secret-key
export DATABASE_URL=sqlite:///site.db
```

## 🧪 Testing

Run the test suite to verify everything works:

```bash
python test_app.py
```

## 📁 Project Structure

```
├── app.py              # Main application
├── config.py           # Configuration settings
├── models.py           # Database models
├── forms.py            # Form definitions
├── routes.py           # Main routes
├── admin.py            # Admin routes
├── run.py              # Application runner
├── admin_pss.py        # Admin setup
├── test_app.py         # Test suite
├── requirements.txt    # Dependencies
├── static/             # CSS, JS, images
└── templates/          # HTML templates
```

## 🆘 Troubleshooting

### Common Issues

1. **Import Errors**: Make sure all dependencies are installed
   ```bash
   pip install -r requirements.txt
   ```

2. **Database Errors**: Delete the `instance/site.db` file and restart
   ```bash
   rm instance/site.db
   python admin_pss.py
   ```

3. **Port Already in Use**: Change the port in `run.py`
   ```python
   app.run(debug=True, host='0.0.0.0', port=5001)
   ```

### Getting Help

- Check the main README.md for detailed documentation
- Run `python test_app.py` to verify installation
- Ensure Python 3.7+ is installed

## 🎯 Next Steps

1. **Change Admin Password**: After first login, change the admin password
2. **Add Real Data**: Create test users and accounts
3. **Customize**: Modify templates and styling as needed
4. **Deploy**: Configure for production deployment

---

**Happy Banking! 🏦** 