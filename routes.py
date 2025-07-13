from flask import Blueprint, render_template, request, redirect, url_for, flash, jsonify, abort
from flask_login import login_user, login_required, logout_user, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime, timedelta
import uuid
from models import db, User, BankAccount, Transaction, InsurancePolicy, InsuranceClaim
from forms import LoginForm, RegisterForm, TransactionForm, InsurancePolicyForm, ClaimForm, AccountForm

routes_bp = Blueprint('routes', __name__)

@routes_bp.route('/')
def index():
    return render_template('index.html')

@routes_bp.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('routes.dashboard'))
    
    form = LoginForm()
    if form.validate_on_submit():
        try:
            user = User.query.filter_by(email=form.email.data).first()
            if user and check_password_hash(user.password_hash, form.password.data):
                if not user.is_active:
                    flash('Account is deactivated. Please contact support.', 'error')
                    return render_template('login.html', form=form)
                
                login_user(user)
                flash('Login successful!', 'success')
                return redirect(url_for('routes.dashboard'))
            else:
                flash('Invalid email or password', 'error')
        except Exception as e:
            flash('An error occurred during login. Please try again.', 'error')
    
    return render_template('login.html', form=form)

@routes_bp.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('routes.dashboard'))
    
    form = RegisterForm()
    if form.validate_on_submit():
        try:
            # Check if email already exists
            if User.query.filter_by(email=form.email.data).first():
                flash('Email already registered', 'error')
                return render_template('register.html', form=form)
            
            # Check if username already exists
            if User.query.filter_by(username=form.username.data).first():
                flash('Username already taken', 'error')
                return render_template('register.html', form=form)
            
            user = User(
                username=form.username.data,
                email=form.email.data,
                password_hash=generate_password_hash(form.password.data),
                first_name=form.first_name.data,
                last_name=form.last_name.data,
                phone=form.phone.data
            )
            db.session.add(user)
            db.session.commit()
            flash('Registration successful! Please login.', 'success')
            return redirect(url_for('routes.login'))
        except Exception as e:
            db.session.rollback()
            flash('An error occurred during registration. Please try again.', 'error')
    
    return render_template('register.html', form=form)

@routes_bp.route('/logout')
@login_required
def logout():
    logout_user()
    flash('You have been logged out.', 'info')
    return redirect(url_for('routes.index'))

@routes_bp.route('/dashboard')
@login_required
def dashboard():
    try:
        accounts = BankAccount.query.filter_by(user_id=current_user.id).all()
        policies = InsurancePolicy.query.filter_by(user_id=current_user.id).all()
        
        # Get recent transactions
        recent_transactions = []
        for account in accounts:
            transactions = Transaction.query.filter_by(account_id=account.id).order_by(Transaction.created_at.desc()).limit(5).all()
            recent_transactions.extend(transactions)
        recent_transactions.sort(key=lambda x: x.created_at, reverse=True)
        recent_transactions = recent_transactions[:10]
        
        # Admin data (only for admin user)
        admin_data = None
        if current_user.username == 'admin':
            admin_data = {
                'users': User.query.all(),
                'accounts': BankAccount.query.all()
            }
        
        return render_template('dashboard.html', 
                             accounts=accounts, 
                             policies=policies, 
                             transactions=recent_transactions,
                             admin_data=admin_data)
    except Exception as e:
        flash('An error occurred while loading dashboard.', 'error')
        return redirect(url_for('routes.index'))

@routes_bp.route('/banking')
@login_required
def banking():
    try:
        accounts = BankAccount.query.filter_by(user_id=current_user.id).all()
        return render_template('banking.html', accounts=accounts)
    except Exception as e:
        flash('An error occurred while loading banking page.', 'error')
        return redirect(url_for('routes.dashboard'))

@routes_bp.route('/insurance')
@login_required
def insurance():
    try:
        policies = InsurancePolicy.query.filter_by(user_id=current_user.id).all()
        return render_template('insurance.html', policies=policies)
    except Exception as e:
        flash('An error occurred while loading insurance page.', 'error')
        return redirect(url_for('routes.dashboard'))

@routes_bp.route('/create_account', methods=['GET', 'POST'])
@login_required
def create_account():
    form = AccountForm()
    if form.validate_on_submit():
        try:
            account_number = f"ACC{datetime.now().strftime('%Y%m%d')}{uuid.uuid4().hex[:8].upper()}"
            account = BankAccount(
                account_number=account_number,
                account_type=form.account_type.data,
                balance=float(form.initial_deposit.data or 0),
                user_id=current_user.id
            )
            db.session.add(account)
            db.session.flush()
            
            # Create initial transaction if deposit > 0
            if form.initial_deposit.data and float(form.initial_deposit.data) > 0:
                transaction = Transaction(
                    transaction_id=f"TXN{uuid.uuid4().hex[:12].upper()}",
                    transaction_type='deposit',
                    amount=float(form.initial_deposit.data),
                    description='Initial deposit',
                    account_id=account.id
                )
                db.session.add(transaction)
            
            db.session.commit()
            flash('Account created successfully!', 'success')
            return redirect(url_for('routes.banking'))
        except Exception as e:
            db.session.rollback()
            flash('An error occurred while creating account. Please try again.', 'error')
    
    return render_template('create_account.html', form=form)

@routes_bp.route('/transaction/<int:account_id>', methods=['GET', 'POST'])
@login_required
def transaction(account_id):
    try:
        account = BankAccount.query.get_or_404(account_id)
        if account.user_id != current_user.id:
            flash('Access denied', 'error')
            return redirect(url_for('routes.banking'))
        
        form = TransactionForm()
        if form.validate_on_submit():
            amount = float(form.amount.data)
            
            # Check sufficient funds for withdrawal
            if form.transaction_type.data == 'withdrawal' and account.balance < amount:
                flash('Insufficient funds', 'error')
                return render_template('transaction.html', form=form, account=account)
            
            # Update account balance
            if form.transaction_type.data == 'deposit':
                account.balance += amount
            elif form.transaction_type.data == 'withdrawal':
                account.balance -= amount
            
            # Create transaction record
            transaction = Transaction(
                transaction_id=f"TXN{uuid.uuid4().hex[:12].upper()}",
                transaction_type=form.transaction_type.data,
                amount=amount,
                description=form.description.data,
                account_id=account.id
            )
            db.session.add(transaction)
            db.session.commit()
            flash('Transaction completed successfully!', 'success')
            return redirect(url_for('routes.banking'))
        
        return render_template('transaction.html', form=form, account=account)
    except Exception as e:
        flash('An error occurred during transaction. Please try again.', 'error')
        return redirect(url_for('routes.banking'))

@routes_bp.route('/create_policy', methods=['GET', 'POST'])
@login_required
def create_policy():
    form = InsurancePolicyForm()
    if form.validate_on_submit():
        try:
            policy = InsurancePolicy(
                policy_number=f"POL{uuid.uuid4().hex[:12].upper()}",
                policy_type=form.policy_type.data,
                coverage_amount=float(form.coverage_amount.data),
                premium_amount=float(form.premium_amount.data),
                start_date=form.start_date.data,
                end_date=form.start_date.data + timedelta(days=365),
                user_id=current_user.id
            )
            db.session.add(policy)
            db.session.commit()
            flash('Insurance policy created successfully!', 'success')
            return redirect(url_for('routes.insurance'))
        except Exception as e:
            db.session.rollback()
            flash('An error occurred while creating policy. Please try again.', 'error')
    
    return render_template('create_policy.html', form=form)

@routes_bp.route('/submit_claim/<int:policy_id>', methods=['GET', 'POST'])
@login_required
def submit_claim(policy_id):
    try:
        policy = InsurancePolicy.query.get_or_404(policy_id)
        if policy.user_id != current_user.id:
            flash('Access denied', 'error')
            return redirect(url_for('routes.insurance'))
        
        form = ClaimForm()
        if form.validate_on_submit():
            claim = InsuranceClaim(
                claim_number=f"CLM{uuid.uuid4().hex[:12].upper()}",
                policy_id=policy.id,
                claim_amount=float(form.claim_amount.data),
                description=form.description.data
            )
            db.session.add(claim)
            db.session.commit()
            flash('Claim submitted successfully!', 'success')
            return redirect(url_for('routes.insurance'))
        
        return render_template('submit_claim.html', form=form, policy=policy)
    except Exception as e:
        flash('An error occurred while submitting claim. Please try again.', 'error')
        return redirect(url_for('routes.insurance'))

@routes_bp.route('/api/account_balance/<int:account_id>')
@login_required
def get_account_balance(account_id):
    try:
        account = BankAccount.query.get_or_404(account_id)
        if account.user_id != current_user.id:
            return jsonify({'error': 'Access denied'}), 403
        
        return jsonify({
            'account_number': account.account_number,
            'balance': account.balance,
            'currency': account.currency
        })
    except Exception as e:
        return jsonify({'error': 'An error occurred'}), 500 