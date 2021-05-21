from warungskuy import app
from flask import render_template, redirect, url_for, flash, request
# Import Item Model
from warungskuy.models import User
# Import Forms
from warungskuy.forms import RegisterForm, LoginForm
# Import Database
from warungskuy import db
# Import login manager
from flask_login import login_user, logout_user, login_required, current_user


@app.route("/")
@app.route("/home")
def home_page():
    return render_template('index.html')


@app.route("/register", methods=['POST', 'GET'])
def register_page():
    form = RegisterForm()
    if form.validate_on_submit():

        user_to_create = User(username=form.username.data,
                              email=form.email.data,
                              password=form.password1.data,
                              phone_number=form.phone_number.data,
                              fullname=form.fullname.data,
                              nik=form.nik.data,
                              address=form.address.data,
                              birth_place=form.birth_place.data,
                              birth_date=form.birth_date.data,
                              gender='L' if form.gender.data == 'Laki-Laki' else 'P',
                              bank=form.bank.data,
                              account_number=form.account_number.data,
                              account_name=form.account_name.data,)

        db.session.add(user_to_create)
        db.session.commit()

        # With successful registration, auto logged in user to market
        # login_user(user_to_create)
        flash(
            f"Account created successfully! You are now logged in as {user_to_create.username}", category="success")

        return redirect(url_for('home_page'))

    if form.errors != {}:  # form.errors return all error from wtform validation inside a dictionary
        for err_msg in form.errors.values():
            flash(f'Error creating user : {err_msg}', category='danger')

    return render_template('register.html', form=form)


@app.route('/login', methods=['POST', 'GET'])
def login_page():
    form = LoginForm()
    if form.validate_on_submit():
        # Check if user is exists
        attempted_user = User.query.filter_by(
            username=form.username.data).first()

        if attempted_user and attempted_user.check_password_correction(
            attempted_password=form.password.data
        ):
            login_user(attempted_user)
            flash(
                f"Success! You're login as {attempted_user.username}", category='success')
            return redirect(url_for('home_page'))

        else:
            flash('Username and password not matched! Please try again',
                  category='danger')

    return render_template('login.html', form=form)

@app.route('/logout')
def logout_page():
    flash("You have been logged out!", category="info")
    logout_user()
    return redirect(url_for('home_page'))
