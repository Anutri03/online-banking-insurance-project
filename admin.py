from flask import Blueprint, render_template, request, redirect, url_for, flash, jsonify, abort
from flask_login import login_required, current_user
from models import db, User, BankAccount, Transaction, InsurancePolicy, InsuranceClaim
from datetime import datetime, timedelta
import json

admin_bp = Blueprint('admin', __name__)

@admin_bp.route('/admin')
@login_required
def admin_dashboard():
    if current_user.username != 'admin':
        abort(403)
    
    try:
        # Get statistics
        total_users = User.query.count()
        total_accounts = BankAccount.query.count()
        total_transactions = Transaction.query.count()
        total_policies = InsurancePolicy.query.count()
        total_claims = InsuranceClaim.query.count()
        
        # Get recent activity
        recent_users = User.query.order_by(User.created_at.desc()).limit(5).all()
        recent_transactions = Transaction.query.order_by(Transaction.created_at.desc()).limit(10).all()
        recent_claims = InsuranceClaim.query.order_by(InsuranceClaim.created_at.desc()).limit(5).all()
        
        # Calculate total balances
        total_balance = sum(account.balance for account in BankAccount.query.all())
        
        # Get system stats
        active_accounts = BankAccount.query.filter_by(status='active').count()
        pending_claims = InsuranceClaim.query.filter_by(status='pending').count()
        
        return render_template('admin/dashboard.html', 
                             total_users=total_users,
                             total_accounts=total_accounts,
                             total_transactions=total_transactions,
                             total_policies=total_policies,
                             total_claims=total_claims,
                             total_balance=total_balance,
                             active_accounts=active_accounts,
                             pending_claims=pending_claims,
                             recent_users=recent_users,
                             recent_transactions=recent_transactions,
                             recent_claims=recent_claims)
    except Exception as e:
        flash('An error occurred while loading admin dashboard.', 'error')
        return redirect(url_for('routes.dashboard'))

@admin_bp.route('/admin/users')
@login_required
def admin_users():
    if current_user.username != 'admin':
        abort(403)
    try:
        users = User.query.all()
        return render_template('admin/users.html', users=users)
    except Exception as e:
        flash('An error occurred while loading users.', 'error')
        return redirect(url_for('admin.admin_dashboard'))

@admin_bp.route('/admin/accounts')
@login_required
def admin_accounts():
    if current_user.username != 'admin':
        abort(403)
    try:
        accounts = BankAccount.query.all()
        return render_template('admin/accounts.html', accounts=accounts)
    except Exception as e:
        flash('An error occurred while loading accounts.', 'error')
        return redirect(url_for('admin.admin_dashboard'))

@admin_bp.route('/admin/transactions')
@login_required
def admin_transactions():
    if current_user.username != 'admin':
        abort(403)
    try:
        transactions = Transaction.query.order_by(Transaction.created_at.desc()).all()
        return render_template('admin/transactions.html', transactions=transactions)
    except Exception as e:
        flash('An error occurred while loading transactions.', 'error')
        return redirect(url_for('admin.admin_dashboard'))

@admin_bp.route('/admin/policies')
@login_required
def admin_policies():
    if current_user.username != 'admin':
        abort(403)
    try:
        policies = InsurancePolicy.query.all()
        return render_template('admin/policies.html', policies=policies)
    except Exception as e:
        flash('An error occurred while loading policies.', 'error')
        return redirect(url_for('admin.admin_dashboard'))

@admin_bp.route('/admin/claims')
@login_required
def admin_claims():
    if current_user.username != 'admin':
        abort(403)
    try:
        claims = InsuranceClaim.query.order_by(InsuranceClaim.created_at.desc()).all()
        return render_template('admin/claims.html', claims=claims)
    except Exception as e:
        flash('An error occurred while loading claims.', 'error')
        return redirect(url_for('admin.admin_dashboard'))

@admin_bp.route('/admin/user/<int:user_id>/edit', methods=['GET', 'POST'])
@login_required
def edit_user(user_id):
    if current_user.username != 'admin':
        abort(403)
    try:
        user = User.query.get_or_404(user_id)
        if request.method == 'POST':
            # Validate input
            username = request.form.get('username', '').strip()
            email = request.form.get('email', '').strip()
            
            if not username or not email:
                flash('Username and email are required.', 'error')
                return render_template('admin/edit_user.html', user=user)
            
            # Check if username/email already exists (excluding current user)
            existing_user = User.query.filter(
                User.username == username,
                User.id != user_id
            ).first()
            if existing_user:
                flash('Username already taken.', 'error')
                return render_template('admin/edit_user.html', user=user)
            
            existing_email = User.query.filter(
                User.email == email,
                User.id != user_id
            ).first()
            if existing_email:
                flash('Email already registered.', 'error')
                return render_template('admin/edit_user.html', user=user)
            
            # Update user
            user.username = username
            user.email = email
            user.first_name = request.form.get('first_name', '').strip()
            user.last_name = request.form.get('last_name', '').strip()
            user.phone = request.form.get('phone', '').strip()
            user.is_active = 'is_active' in request.form
            
            db.session.commit()
            flash('User updated successfully!', 'success')
            return redirect(url_for('admin.admin_users'))
        
        return render_template('admin/edit_user.html', user=user)
    except Exception as e:
        flash('An error occurred while updating user.', 'error')
        return redirect(url_for('admin.admin_users'))

@admin_bp.route('/admin/user/<int:user_id>/delete', methods=['POST'])
@login_required
def delete_user(user_id):
    if current_user.username != 'admin':
        abort(403)
    try:
        user = User.query.get_or_404(user_id)
        if user.username == 'admin':
            flash('Cannot delete admin user!', 'error')
            return redirect(url_for('admin.admin_users'))
        
        db.session.delete(user)
        db.session.commit()
        flash('User deleted successfully!', 'success')
        return redirect(url_for('admin.admin_users'))
    except Exception as e:
        db.session.rollback()
        flash('An error occurred while deleting user.', 'error')
        return redirect(url_for('admin.admin_users'))

@admin_bp.route('/admin/account/<int:account_id>/edit', methods=['GET', 'POST'])
@login_required
def edit_account(account_id):
    if current_user.username != 'admin':
        abort(403)
    try:
        account = BankAccount.query.get_or_404(account_id)
        if request.method == 'POST':
            try:
                balance = float(request.form.get('balance', 0))
                if balance < 0:
                    flash('Balance cannot be negative.', 'error')
                    return render_template('admin/edit_account.html', account=account)
                
                account.balance = balance
                account.status = request.form.get('status', 'active')
                db.session.commit()
                flash('Account updated successfully!', 'success')
                return redirect(url_for('admin.admin_accounts'))
            except ValueError:
                flash('Invalid balance amount.', 'error')
                return render_template('admin/edit_account.html', account=account)
        
        return render_template('admin/edit_account.html', account=account)
    except Exception as e:
        flash('An error occurred while updating account.', 'error')
        return redirect(url_for('admin.admin_accounts'))

@admin_bp.route('/admin/account/<int:account_id>/delete', methods=['POST'])
@login_required
def delete_account(account_id):
    if current_user.username != 'admin':
        abort(403)
    try:
        account = BankAccount.query.get_or_404(account_id)
        # Delete all transactions for this account first
        Transaction.query.filter_by(account_id=account.id).delete()
        db.session.delete(account)
        db.session.commit()
        flash('Account deleted successfully!', 'success')
        return redirect(url_for('admin.admin_accounts'))
    except Exception as e:
        db.session.rollback()
        flash('An error occurred while deleting account.', 'error')
        return redirect(url_for('admin.admin_accounts'))

@admin_bp.route('/admin/claim/<int:claim_id>/process', methods=['POST'])
@login_required
def process_claim(claim_id):
    if current_user.username != 'admin':
        abort(403)
    try:
        claim = InsuranceClaim.query.get_or_404(claim_id)
        action = request.form.get('action')
        
        if action == 'approve':
            claim.status = 'approved'
            claim.processed_at = datetime.utcnow()
            flash('Claim approved successfully!', 'success')
        elif action == 'reject':
            claim.status = 'rejected'
            claim.processed_at = datetime.utcnow()
            flash('Claim rejected successfully!', 'success')
        else:
            flash('Invalid action.', 'error')
            return redirect(url_for('admin.admin_claims'))
        
        db.session.commit()
        return redirect(url_for('admin.admin_claims'))
    except Exception as e:
        flash('An error occurred while processing claim.', 'error')
        return redirect(url_for('admin.admin_claims'))

@admin_bp.route('/admin/system_state')
@login_required
def system_state():
    if current_user.username != 'admin':
        abort(403)
    
    try:
        # System statistics
        stats = {
            'users': {
                'total': User.query.count(),
                'active': User.query.filter_by(is_active=True).count(),
                'new_this_month': User.query.filter(User.created_at >= datetime.now().replace(day=1)).count()
            },
            'accounts': {
                'total': BankAccount.query.count(),
                'active': BankAccount.query.filter_by(status='active').count(),
                'savings': BankAccount.query.filter_by(account_type='savings').count(),
                'checking': BankAccount.query.filter_by(account_type='checking').count()
            },
            'transactions': {
                'total': Transaction.query.count(),
                'this_month': Transaction.query.filter(Transaction.created_at >= datetime.now().replace(day=1)).count(),
                'total_volume': sum(t.amount for t in Transaction.query.all())
            },
            'policies': {
                'total': InsurancePolicy.query.count(),
                'active': InsurancePolicy.query.filter_by(status='active').count(),
                'total_coverage': sum(p.coverage_amount for p in InsurancePolicy.query.all())
            },
            'claims': {
                'total': InsuranceClaim.query.count(),
                'pending': InsuranceClaim.query.filter_by(status='pending').count(),
                'approved': InsuranceClaim.query.filter_by(status='approved').count(),
                'rejected': InsuranceClaim.query.filter_by(status='rejected').count()
            }
        }
        
        return render_template('admin/system_state.html', stats=stats)
    except Exception as e:
        flash('An error occurred while loading system state.', 'error')
        return redirect(url_for('admin.admin_dashboard'))

@admin_bp.route('/admin/analytics')
@login_required
def analytics():
    if current_user.username != 'admin':
        abort(403)
    
    try:
        # Get data for charts
        monthly_users = []
        monthly_transactions = []
        monthly_balance = []
        
        for i in range(6):
            date = datetime.now() - timedelta(days=30*i)
            month_start = date.replace(day=1)
            month_end = (month_start + timedelta(days=32)).replace(day=1) - timedelta(days=1)
            
            users_count = User.query.filter(
                User.created_at >= month_start,
                User.created_at <= month_end
            ).count()
            
            transactions_count = Transaction.query.filter(
                Transaction.created_at >= month_start,
                Transaction.created_at <= month_end
            ).count()
            
            total_balance = sum(account.balance for account in BankAccount.query.all())
            
            monthly_users.append(users_count)
            monthly_transactions.append(transactions_count)
            monthly_balance.append(total_balance)
        
        chart_data = {
            'labels': ['6 months ago', '5 months ago', '4 months ago', '3 months ago', '2 months ago', 'Last month'],
            'users': monthly_users[::-1],
            'transactions': monthly_transactions[::-1],
            'balance': monthly_balance[::-1]
        }
        
        return render_template('admin/analytics.html', chart_data=chart_data)
    except Exception as e:
        flash('An error occurred while loading analytics.', 'error')
        return redirect(url_for('admin.admin_dashboard'))

@admin_bp.route('/admin/export/users')
@login_required
def export_users():
    if current_user.username != 'admin':
        abort(403)
    try:
        users = User.query.all()
        data = '\n'.join([f'{u.id},{u.username},{u.email},{u.first_name},{u.last_name},{u.created_at}' for u in users])
        return data, 200, {'Content-Type': 'text/csv', 'Content-Disposition': 'attachment; filename=users.csv'}
    except Exception as e:
        flash('An error occurred while exporting users.', 'error')
        return redirect(url_for('admin.admin_users'))

@admin_bp.route('/admin/export/accounts')
@login_required
def export_accounts():
    if current_user.username != 'admin':
        abort(403)
    try:
        accounts = BankAccount.query.all()
        data = '\n'.join([f'{a.id},{a.account_number},{a.account_type},{a.balance},{a.status},{a.user.username}' for a in accounts])
        return data, 200, {'Content-Type': 'text/csv', 'Content-Disposition': 'attachment; filename=accounts.csv'}
    except Exception as e:
        flash('An error occurred while exporting accounts.', 'error')
        return redirect(url_for('admin.admin_accounts'))

@admin_bp.route('/admin/export/transactions')
@login_required
def export_transactions():
    if current_user.username != 'admin':
        abort(403)
    try:
        transactions = Transaction.query.all()
        data = '\n'.join([f'{t.id},{t.transaction_id},{t.transaction_type},{t.amount},{t.created_at},{t.account.account_number}' for t in transactions])
        return data, 200, {'Content-Type': 'text/csv', 'Content-Disposition': 'attachment; filename=transactions.csv'}
    except Exception as e:
        flash('An error occurred while exporting transactions.', 'error')
        return redirect(url_for('admin.admin_transactions'))

@admin_bp.route('/admin/api/stats')
@login_required
def api_stats():
    if current_user.username != 'admin':
        abort(403)
    
    try:
        stats = {
            'total_users': User.query.count(),
            'total_accounts': BankAccount.query.count(),
            'total_balance': sum(account.balance for account in BankAccount.query.all()),
            'pending_claims': InsuranceClaim.query.filter_by(status='pending').count(),
            'active_policies': InsurancePolicy.query.filter_by(status='active').count()
        }
        
        return jsonify(stats)
    except Exception as e:
        return jsonify({'error': 'An error occurred'}), 500 