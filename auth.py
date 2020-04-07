"""Routes for user authentication."""
from flask import Blueprint, render_template, request
from flask_login import login_required, logout_user, current_user, login_user
from flask import current_app as app
from app import User, db


# Blueprint Configuration
auth_bp = Blueprint('auth_bp', __name__,
                    template_folder='templates',
                    static_folder='static')


@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
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
            
    return render_template('register.html')
