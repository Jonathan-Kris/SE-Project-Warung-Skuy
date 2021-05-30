from warungskuy import app
from flask import render_template, redirect, url_for, flash, request, session
# Import Item Model
from warungskuy.models import User, Lender, Borrower
# Import Forms
from warungskuy.forms import RegisterBorrowerForm, RegisterLenderForm, LoginForm
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
    lenderForm = RegisterLenderForm()
    borrowerForm = RegisterBorrowerForm()

    if lenderForm.validate_on_submit():
        if lenderForm.nik.data:
            user_to_create = Lender(username=lenderForm.username.data,
                                email=lenderForm.email.data,
                                password=lenderForm.password1.data,
                                phone_number=lenderForm.phone_number.data,
                                fullname=lenderForm.fullname.data,
                                nik=lenderForm.nik.data,
                                address=lenderForm.address.data,
                                birth_place=lenderForm.birth_place.data,
                                birth_date=lenderForm.birth_date.data,
                                gender='L' if lenderForm.gender.data == 'Laki-Laki' else 'P',
                                bank=lenderForm.bank.data,
                                account_number=lenderForm.account_number.data,
                                account_name=lenderForm.account_name.data,)

        db.session.add(user_to_create)
        db.session.commit()

        # Adding Session
        session['account_type'] = 'Lender'

        # With successful registration, auto logged in user to market
        # login_user(user_to_create)
        flash(
            f"Account created successfully! You are now logged in as {user_to_create.username}", category="success")

        return redirect(url_for('login_page'))

    if borrowerForm.validate_on_submit():
        user_to_create = Borrower(
                            username=borrowerForm.username.data,
                            email=borrowerForm.email.data,
                            password=borrowerForm.password1.data,
                            phone_number=borrowerForm.phone_number.data,
                            fullname=borrowerForm.fullname.data,
                            birth_place=borrowerForm.birth_place.data,
                            birth_date=borrowerForm.birth_date.data,
                            gender='L' if borrowerForm.gender.data == 'Laki-Laki' else 'P',
                            )

        db.session.add(user_to_create)
        db.session.commit()

        # Adding Session
        session['account_type'] = 'Borrower'

        # With successful registration, auto logged in user to market login_user(user_to_create)
        flash(
            f"Account created successfully! You are now logged in as {user_to_create.username}", category="success")

        return redirect(url_for('login_page'))

    return render_template('register.html',  lenderForm=lenderForm, borrowerForm=borrowerForm,)


@app.route('/login', methods=['POST', 'GET'])
def login_page():
    form = LoginForm()
    if form.validate_on_submit():
        # Check if user is exists
        lender = Lender.query.filter_by(username=form.username.data).first()
        borrower = Borrower.query.filter_by(username=form.username.data).first()

        if(lender):
            attempted_user = lender
        elif(borrower):
            attempted_user = borrower
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

@app.route('/pinjaman')
def pinjaman_page():
    return render_template('pinjaman/main.html')

@app.route('/cara-kerja')
def cara_kerja_page():
    return render_template('cara-kerja.html')
