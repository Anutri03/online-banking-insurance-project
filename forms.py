from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, SelectField, DecimalField, TextAreaField, DateField
from wtforms.validators import DataRequired, Email, Length, EqualTo, NumberRange, Optional
from datetime import date

class LoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Login')

class RegisterForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), Length(min=3, max=20)])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired(), Length(min=6)])
    confirm_password = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password')])
    first_name = StringField('First Name', validators=[DataRequired(), Length(max=50)])
    last_name = StringField('Last Name', validators=[DataRequired(), Length(max=50)])
    phone = StringField('Phone Number', validators=[Optional(), Length(max=20)])
    submit = SubmitField('Register')

class TransactionForm(FlaskForm):
    transaction_type = SelectField('Transaction Type', choices=[
        ('deposit', 'Deposit'),
        ('withdrawal', 'Withdrawal'),
        ('transfer', 'Transfer')
    ], validators=[DataRequired()])
    amount = DecimalField('Amount', validators=[DataRequired(), NumberRange(min=0.01, message='Amount must be greater than 0')])
    description = StringField('Description', validators=[Optional(), Length(max=200)])
    submit = SubmitField('Submit Transaction')

class InsurancePolicyForm(FlaskForm):
    policy_type = SelectField('Policy Type', choices=[
        ('life', 'Life Insurance'),
        ('health', 'Health Insurance'),
        ('auto', 'Auto Insurance'),
        ('home', 'Home Insurance')
    ], validators=[DataRequired()])
    coverage_amount = DecimalField('Coverage Amount', validators=[DataRequired(), NumberRange(min=1000, message='Coverage amount must be at least $1,000')])
    premium_amount = DecimalField('Premium Amount', validators=[DataRequired(), NumberRange(min=10, message='Premium amount must be at least $10')])
    start_date = DateField('Start Date', validators=[DataRequired()], default=date.today)
    submit = SubmitField('Create Policy')

class ClaimForm(FlaskForm):
    claim_amount = DecimalField('Claim Amount', validators=[DataRequired(), NumberRange(min=0.01, message='Claim amount must be greater than 0')])
    description = TextAreaField('Description', validators=[DataRequired(), Length(min=10, max=1000, message='Description must be between 10 and 1000 characters')])
    submit = SubmitField('Submit Claim')

class AccountForm(FlaskForm):
    account_type = SelectField('Account Type', choices=[
        ('savings', 'Savings Account'),
        ('checking', 'Checking Account'),
        ('business', 'Business Account')
    ], validators=[DataRequired()])
    initial_deposit = DecimalField('Initial Deposit', validators=[Optional(), NumberRange(min=0, message='Initial deposit cannot be negative')])
    submit = SubmitField('Create Account') 