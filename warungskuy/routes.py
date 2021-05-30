from warungskuy import app
from flask import render_template, redirect, url_for, flash, request, session
# Import Item Model
from warungskuy.models import User, Investor, Peminjam
# Import Forms
from warungskuy.forms import RegisterPeminjamForm, RegisterInvestorForm, LoginForm
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
    investorForm = RegisterInvestorForm()
    peminjamForm = RegisterPeminjamForm()

    if investorForm.validate_on_submit():
        if investorForm.nik.data:
            user_to_create = Investor(username=investorForm.username.data,
                                email=investorForm.email.data,
                                password=investorForm.password1.data,
                                phone_number=investorForm.phone_number.data,
                                fullname=investorForm.fullname.data,
                                nik=investorForm.nik.data,
                                address=investorForm.address.data,
                                birth_place=investorForm.birth_place.data,
                                birth_date=investorForm.birth_date.data,
                                gender='L' if investorForm.gender.data == 'Laki-Laki' else 'P',
                                bank=investorForm.bank.data,
                                account_number=investorForm.account_number.data,
                                account_name=investorForm.account_name.data,)

        db.session.add(user_to_create)
        db.session.commit()

        # Adding Session
        session['account_type'] = 'Investor'

        # With successful registration, auto logged in user to market
        # login_user(user_to_create)
        flash(
            f"Account created successfully! You are now logged in as {user_to_create.username}", category="success")

        return redirect(url_for('login_page'))

    if peminjamForm.validate_on_submit():
        user_to_create = Peminjam(
                            username=peminjamForm.username.data,
                            email=peminjamForm.email.data,
                            password=peminjamForm.password1.data,
                            phone_number=peminjamForm.phone_number.data,
                            fullname=peminjamForm.fullname.data,
                            birth_place=peminjamForm.birth_place.data,
                            birth_date=peminjamForm.birth_date.data,
                            gender='L' if peminjamForm.gender.data == 'Laki-Laki' else 'P',
                            )

        db.session.add(user_to_create)
        db.session.commit()

        # Adding Session
        session['account_type'] = 'Peminjam'

        # With successful registration, auto logged in user to market login_user(user_to_create)
        flash(
            f"Account created successfully! You are now logged in as {user_to_create.username}", category="success")

        return redirect(url_for('login_page'))

    return render_template('register.html',  investorForm=investorForm, peminjamForm=peminjamForm,)


@app.route('/login', methods=['POST', 'GET'])
def login_page():
    form = LoginForm()
    if form.validate_on_submit():
        # Check if user is exists
        investor = Investor.query.filter_by(username=form.username.data).first()
        peminjam = Peminjam.query.filter_by(username=form.username.data).first()

        if(investor):
            attempted_user = investor
        elif(peminjam):
            attempted_user = peminjam
        else:
            attempted_user = None

        if attempted_user and attempted_user.check_password_correction(
            attempted_password=form.password.data
        ):
            login_user(attempted_user)
            print(current_user)
            flash(
                f"Success! You're login as {attempted_user.username}", category='success')
            return redirect(url_for('home_page'))

        else:
            flash('Username and password not matched! Please try again',
                  category='danger')

    return render_template('login.html', form=form, current_user=current_user)

@app.route('/logout')
def logout_page():
    flash("You have been logged out!", category="info")
    logout_user()
    return redirect(url_for('home_page'))

@app.route('/pendanaan')
def pendanaan_page():
    return render_template('pendanaan.html')

@app.route('/peminjaman')
def peminjaman_page():
    return render_template('peminjaman.html')

@app.route('/cara-kerja')
def cara_kerja_page():
    return render_template('cara-kerja.html')
