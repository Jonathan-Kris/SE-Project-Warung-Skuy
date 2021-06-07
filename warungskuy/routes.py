from warungskuy import app
from flask import render_template, redirect, url_for, flash, request, session
# Import Item Model
from warungskuy.models import Borrower, Lender, LendingTransaction, Loan, User
# Import Forms
from warungskuy.forms import LendingForm, LoanForm, LoginForm, RegisterBorrowerForm, RegisterLenderForm
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
        if lenderForm.bank.data == 'XXXXXX':
            err_Bank = "Please select a bank"
            return redirect(url_for('login_page'), errBank = err_Bank)

        user_to_create = Lender(username=lenderForm.username.data,
                            email=lenderForm.email.data,
                            #password=lenderForm.password1.data, #DISABLE FOR TESTING PURPOSE ONLY
                            password_hash=borrowerForm.password1.data,
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

        flash(
            f"Account created successfully! You are now logged in as {user_to_create.username}", category="success")

        # With successful registration, redirect user to login page
        return redirect(url_for('login_page'))

    if borrowerForm.validate_on_submit():
        user_to_create = Borrower(
                            username=borrowerForm.username.data,
                            email=borrowerForm.email.data,
                            #password=borrowerForm.password1.data, #DISABLE FOR TESTING PURPOSE ONLY
                            password_hash=borrowerForm.password1.data,
                            phone_number=borrowerForm.phone_number.data,
                            fullname=borrowerForm.fullname.data,
                            birth_place=borrowerForm.birth_place.data,
                            birth_date=borrowerForm.birth_date.data,
                            gender='L' if borrowerForm.gender.data == 'Laki-Laki' else 'P',
                            )

        db.session.add(user_to_create)
        db.session.commit()

        flash(
            f"Account created successfully! You are now logged in as {user_to_create.username}", category="success")

        # With successful registration, redirect user to login page
        return redirect(url_for('login_page'))

    return render_template('register.html',  lenderForm=lenderForm, borrowerForm=borrowerForm,)


@app.route('/login', methods=['POST', 'GET'])
def login_page():
    form = LoginForm()
    if form.validate_on_submit():
        # Check if user is exists
        lender = Lender.query.filter_by(username=form.username.data).first()
        borrower = Borrower.query.filter_by(username=form.username.data).first()

        print('Lender :', lender)
        print('Borrower :', borrower)

        if(lender):
            attempted_user = lender
        elif(borrower):
            attempted_user = borrower
        else:
            flash(f"Oops! Sorry there are problems detecting the user")

        # print(attempted_user.password_hash)
        # DISABLED FOR EASE OF TESTING PURPOSE
        # if attempted_user and attempted_user.check_password_correction(
        #     attempted_password=form.password.data
        # ):

        if (attempted_user and attempted_user.password_hash == form.password.data):
            login_user(attempted_user)
            print('Current User : ', current_user.username)
            flash(
                f"Success! You're login as {current_user.username}", category='success')
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

@app.route('/pendanaan')
def pendanaan_page():
    if current_user.is_authenticated:
        items_pendanaan = Loan.query.all()
        items_ongoing =  Loan.query\
            .join(LendingTransaction, Loan.id == LendingTransaction.loan_id)\
            .filter(LendingTransaction.lender_id == current_user.id)
            # .filter(Loan.borrower == LendingTransaction.lender_id)\

        # Could pose performance issue as data gets larger, but will do later. Can be solved by adding counter field in the db
        # https://stackoverflow.com/questions/16000287/how-to-get-length-of-or-count-of-datastore-entities-through-a-reference-collec
        count_items_pendanaan = Loan.query.count()
        count_items_ongoing = Loan.query\
            .join(LendingTransaction, Loan.id == LendingTransaction.loan_id)\
            .filter(LendingTransaction.lender_id == current_user.id)\
            .count()

        return render_template('pendanaan/main.html', itemsPendanaan = items_pendanaan, itemsOngoing = items_ongoing,\
            countItemsPendanaan = count_items_pendanaan, countItemsOngoing = count_items_ongoing)
    else:
        return render_template('pendanaan/main.html')

@app.route('/pendanaan/detail/<loan_id>')
def pendanaan_detail_page(loan_id):
    loan_detail = Loan.query.filter_by(id=loan_id).first()

    return render_template('pendanaan/detail.html', loanDetail = loan_detail)

@app.route('/pendanaan/form-pemberian/<loan_id>', methods=['POST', 'GET'])
def pendanaan_form_pemberian_page(loan_id):
    loan_detail = Loan.query.filter_by(id=loan_id).first()

    print(loan_detail)

    form = LendingForm()
    
    if form.validate_on_submit():
        print(form.lending_amount.data)

        lendingTr = LendingTransaction(
            lender_id=current_user.id,
            loan_id=loan_id,
            lending_amount=form.lending_amount.data
        )

        print(lendingTr)

        db.session.add(lendingTr)
        db.session.commit()

        return redirect(url_for('pendanaan_detail_page', loan_id = loan_id))

    return render_template('pendanaan/form-pemberian.html', form=form, loanDetail = loan_detail)

@app.route('/pinjaman')
def pinjaman_main_page():
    if current_user.is_authenticated:
        items_pinjaman_user = Loan.query\
            .join(LendingTransaction, Loan.id == LendingTransaction.loan_id)\
            .filter(Loan.borrower == current_user.id)
            # .filter(Loan.borrower == LendingTransaction.lender_id)\

        # Could pose performance issue as data gets larger, but will do later. Can be solved by adding counter field in the db
        # https://stackoverflow.com/questions/16000287/how-to-get-length-of-or-count-of-datastore-entities-through-a-reference-collec
        count_items_pinjaman_user = Loan.query\
            .join(LendingTransaction, Loan.id == LendingTransaction.loan_id)\
            .filter(Loan.borrower == current_user.id)\
            .count()
        
        return render_template('pinjaman/main.html', itemsPinjamanUser = items_pinjaman_user,\
            countItemsPinjamanUser = count_items_pinjaman_user)
    else:
        return render_template('pinjaman/main.html')



@app.route('/pinjaman/pengajuan', methods=['POST', 'GET'])
def pinjaman_pengajuan_page():
    form = LoanForm()

    if form.validate_on_submit():
        loan_to_create = Loan(title=form.title.data,
                            tenor=form.tenor.data,
                            start_loan=form.start_loan.data,
                            end_loan=form.end_loan.data,
                            nominal=form.nominal.data,
                            interest=form.interest.data,
                            loan_reason=form.loan_reason.data,
                            business_desc=form.business_desc.data,
                            location=form.location.data,
                            start_year=form.start_year.data,
                            business_address=form.business_address.data,
                            gross_income=form.gross_income.data,
                            net_income=form.net_income.data,
                            modal=form.modal.data,
                            borrower=current_user.id,
                            )

        db.session.add(loan_to_create)
        db.session.commit()

        # With successful registration, auto logged in user to market
        # login_user(user_to_create)
        flash(
            f"Loan request successfully created!", category="success")

        return redirect(url_for('pinjaman_main_page'))

    return render_template('pinjaman/pengajuan.html', form=form)

@app.route('/cara-kerja')
def cara_kerja_page():
    return render_template('cara-kerja.html')