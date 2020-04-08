"""Routes for user authentication."""
from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_required, logout_user, current_user, login_user
from flask import current_app as app
from app import User, db, login_manager


# Blueprint Configuration
auth_bp = Blueprint('auth_bp', __name__,
                    template_folder='templates',
                    static_folder='static')


@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))  # Bypass if user is logged in

    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        user = User.query.filter_by(email=email).first()  # Validate Login Attempt
        if user and user.check_password(password=password):
            login_user(user)
            next_page = request.args.get('next')
            return redirect(next_page or url_for('index'))
        flash('Invalid username/password combination')
        return redirect(url_for('auth_bp.login'))
    elif request.method == 'GET':
        if current_user.is_authenticated:
            return redirect(url_for('index'))
        return render_template('login.html')


@auth_bp.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        password = request.form['password']
        confirm_password = request.form['confirm']

        existing_user = User.query.filter_by(email=email).first()  # Check if user exists

        if (password != confirm_password):
            return render_template(
                'register.html',
                error = "passwords don't match"
            )
        elif existing_user is not None:
            return render_template(
                'register.html',
                error = "Account already exists with that email"
            )
        else:
            user = User(name=name,
                        email=email)
            user.set_password(password)
            db.session.add(user)
            db.session.commit()  # Create new user
            login_user(user)
            return redirect(url_for('index'))
    elif request.method == 'GET':
        if current_user.is_authenticated:
            return redirect(url_for('index'))
        return render_template('register.html')

@auth_bp.route("/logout")
@login_required
def logout():
    """User log-out logic."""
    logout_user()
    return redirect(url_for('index'))