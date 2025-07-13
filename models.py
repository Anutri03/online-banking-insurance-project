from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from datetime import datetime
import uuid

db = SQLAlchemy()

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(120), nullable=False)
    first_name = db.Column(db.String(50), nullable=False)
    last_name = db.Column(db.String(50), nullable=False)
    phone = db.Column(db.String(20))
    date_of_birth = db.Column(db.Date)
    address = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    is_active = db.Column(db.Boolean, default=True)
    
    # Relationships
    bank_accounts = db.relationship('BankAccount', backref='user', lazy=True, cascade='all, delete-orphan')
    insurance_policies = db.relationship('InsurancePolicy', backref='user', lazy=True, cascade='all, delete-orphan')

    def __repr__(self):
        return f'<User {self.username}>'

class BankAccount(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    account_number = db.Column(db.String(20), unique=True, nullable=False)
    account_type = db.Column(db.String(20), nullable=False)
    balance = db.Column(db.Float, default=0.0)
    currency = db.Column(db.String(3), default='USD')
    status = db.Column(db.String(20), default='active')
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id', ondelete='CASCADE'), nullable=False)
    
    # Relationships
    transactions = db.relationship('Transaction', backref='account', lazy=True, cascade='all, delete-orphan')

    def __repr__(self):
        return f'<BankAccount {self.account_number}>'

class Transaction(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    transaction_id = db.Column(db.String(50), unique=True, nullable=False)
    transaction_type = db.Column(db.String(20), nullable=False)
    amount = db.Column(db.Float, nullable=False)
    description = db.Column(db.String(200))
    status = db.Column(db.String(20), default='completed')
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    account_id = db.Column(db.Integer, db.ForeignKey('bank_account.id', ondelete='CASCADE'), nullable=False)

    def __repr__(self):
        return f'<Transaction {self.transaction_id}>'

class InsurancePolicy(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    policy_number = db.Column(db.String(20), unique=True, nullable=False)
    policy_type = db.Column(db.String(50), nullable=False)
    coverage_amount = db.Column(db.Float, nullable=False)
    premium_amount = db.Column(db.Float, nullable=False)
    start_date = db.Column(db.Date, nullable=False)
    end_date = db.Column(db.Date, nullable=False)
    status = db.Column(db.String(20), default='active')
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id', ondelete='CASCADE'), nullable=False)
    
    # Relationships
    claims = db.relationship('InsuranceClaim', backref='policy', lazy=True, cascade='all, delete-orphan')

    def __repr__(self):
        return f'<InsurancePolicy {self.policy_number}>'

class InsuranceClaim(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    claim_number = db.Column(db.String(20), unique=True, nullable=False)
    policy_id = db.Column(db.Integer, db.ForeignKey('insurance_policy.id', ondelete='CASCADE'), nullable=False)
    claim_amount = db.Column(db.Float, nullable=False)
    description = db.Column(db.Text, nullable=False)
    status = db.Column(db.String(20), default='pending')
    submitted_at = db.Column(db.DateTime, default=datetime.utcnow)
    processed_at = db.Column(db.DateTime)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f'<InsuranceClaim {self.claim_number}>' 