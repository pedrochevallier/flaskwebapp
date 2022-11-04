from flask import Blueprint, render_template, request, flash, redirect, url_for
from .models import Pendings, User, Person, Cvs
from werkzeug.security import generate_password_hash, check_password_hash
from . import db, UPLOAD_FOLDER, ALLOWED_EXTENSIONS
from flask_login import login_user, login_required, logout_user, current_user
from werkzeug.utils import secure_filename
from datetime import date

import os


auth = Blueprint('auth', __name__)


@auth.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        # if user is logged in redirect to home
        return redirect(url_for('views.home'))
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        user = User.query.filter_by(email=email).first()
        if user:
            if check_password_hash(user.password, password):
                login_user(user, remember=True)
                return redirect(url_for('views.home'))
            else:
                flash('Wrong password. Please try again', category='error')
        else:
            flash('Email does not exist', category='error')

    return render_template("login.html", user=current_user)


@auth.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('auth.login'))


@auth.route('/sign-up', methods=['GET', 'POST'])
def sign_up():

    if request.method == 'POST':
        email = request.form.get('email')
        first_name = request.form.get('firstName')
        password1 = request.form.get('password1')
        password2 = request.form.get('password2')

        user = User.query.filter_by(email=email).first()
        if user:
            flash('Email already registered', category='error')
        elif len(email) < 4:
            flash('Email must have more than 4 characters', 'error')
        elif len(first_name) < 2:
            flash('Name must have more than 2 characters.', 'error')
        elif password1 != password2:
            flash('Passwords do not match.', category='error')
        elif len(password1) < 7:
            flash('Password must have at least 7 characters', 'error')
        else:
            # place the user on pending approval from admin
            user = Pendings(email=email, first_name=first_name, password=generate_password_hash(password1, method='sha256'))
            db.session.add(user)
            db.session.commit()
            return render_template("pending.html")

    return render_template("sign_up.html", user=current_user)


@auth.route('/authuser/<id>', methods=['GET', 'POST'])
@login_required
def auth_user(id):
    pending = Pendings.query.filter_by(id=id).first()
    user = User(email=pending.email, first_name=pending.first_name, password=pending.password)
    db.session.add(user)
    db.session.commit()
    delete = Pendings.query.filter_by(id=id).delete()
    db.session.commit()
    return redirect("/admin")


@auth.route('/deleteuser/<id>', methods=['GET', 'POST'])
@login_required
def delete_user(id):
    delete = User.query.filter_by(id=id).delete()
    db.session.commit()
    return redirect("/admin")


@auth.route('/<uniqueID>', methods=['POST', 'GET'])
def cv_download(uniqueID):
    person = Person.query.filter_by(uniqueID=uniqueID).first()
    id = person.id

    loaded_cvs = Cvs.query.filter_by(person_id=id)

    return render_template('download.html', id=id, loaded=loaded_cvs)
