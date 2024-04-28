from flask import Blueprint, render_template, request, redirect, flash, url_for
from .models import User
from werkzeug.security import generate_password_hash, check_password_hash
from . import db
from flask_login import login_user, logout_user, login_required, current_user

auth = Blueprint('auth', __name__)


@auth.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']

        user = User.query.filter_by(email=email).first()
        if user:
            if check_password_hash(user.password, password):
                flash('Logged in successfully!', category='success')
                login_user(user, remember=True)
                return redirect(url_for('views.home'))
            else:
                flash('Wrong password', category='error')
        else:
            flash('Email Does Not Exist', category='error')

    return render_template('login.html', user=current_user)


@auth.route('/logout')
@login_required
def logout_page():
    logout_user()
    return redirect(url_for('auth.login'))


@auth.route('/signup', methods=['GET', 'POST'])
def signup_page():
    if request.method == 'POST':
        email = request.form.get('email')
        password1 = request.form.get('password1')
        password2 = request.form.get('password2')
        first_name = request.form.get('first_name')

        user = User.query.filter_by(email=email).first()
        if user:
            flash('Email Already Exists', category='error')
        elif len(email) < 4:
            flash('Email Must be at least 4 characters long', category='error')

        elif len(first_name) < 2:
            flash('First must be at least 2 characters long', category='error')

        elif len(password1) < 7:
            flash('Password must be at least 7 characters long')
        elif password2 != password1:
            flash('Passwords must match', category='error')
        else:
            new_user = User(email=email, first_name=first_name, password=generate_password_hash(password1, method='pbkdf2:sha256'))
            db.session.add(new_user)
            try:
                db.session.commit()
            except Exception as e:
                db.session.rollback()
                flash('Something went wrong. Error{}'.format(e))
                return redirect(url_for('signup_page'))
            login_user(new_user, remember=True)
            flash('Congratulations! Account created successfully!', category='success')
            return redirect(url_for('views.home'))

    return render_template('sign_up.html', user=current_user)
