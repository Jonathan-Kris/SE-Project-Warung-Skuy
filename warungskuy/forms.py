from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, RadioField, SelectField
from wtforms.validators import Length, EqualTo, Email, DataRequired, ValidationError
from wtforms.fields.html5 import DateField
from warungskuy.models import User, Lender, Borrower

class RegisterLenderForm(FlaskForm):

    # Function to catch input error
    # The name validate_[field] is the convention in Flask, so FlaskForm understand this
    # validation is for username
    def validate_username(self, username_to_check):
        user = Lender.query.filter_by(username=username_to_check.data).first()
        if(user):
            raise ValidationError('Username telah digunakan')

    def validate_email(self, email_to_check):
        email = Lender.query.filter_by(email=email_to_check.data).first()
        if(email):
            raise ValidationError('Email ini telah digunakan')

    def validate_nik(self, nik_to_check):
        nik = Lender.query.filter_by(nik=nik_to_check.data).first()
        if(nik):
            raise ValidationError('NIK ini telah terasosiasi dengan user lain')

    username = StringField(label='User Name', validators=[
                           Length(min=2, max=30), DataRequired()])
    email = StringField(label='Email', validators=[
                        Email(), DataRequired()])
    password1 = PasswordField(label='Password', validators=[
                              Length(min=6), DataRequired()])
    password2 = PasswordField(label='Konfirmasi Password', validators=[
                              EqualTo('password1'), DataRequired()])
    phone_number = StringField(label='Kontak Telepon', validators=[
        Length(min=11, max=13), DataRequired()])
    fullname = StringField(label='Nama Lengkap', validators=[
                           Length(min=2, max=100), DataRequired()])                      
    nik = StringField(label='Nomor Induk Kependudukan', validators=[
        Length(min=16, max=16), DataRequired()])
    address = StringField(label='Alamat Lengkap (Sesuai KTP)', validators=[
        DataRequired()])
    birth_place = StringField(label='Tempat Lahir', validators=[
        DataRequired()])
    birth_date = DateField('Tanggal Lahir', format='%Y-%m-%d', validators=[
        DataRequired()])
    gender = RadioField(label='Jenis Kelamin', choices=['Laki-Laki', 'Perempuan'], validators=[
        DataRequired()])
    bank = SelectField(u'Bank', choices=[('bbca', 'Bank Central Asia'),
                                         ('bmri', 'Bank Mandiri'),
                                         ('bbri', 'Bank Rakyat Indonesia')], 
                                         validators=[DataRequired()])
    account_number = StringField(
        label='Nomor Rekening', validators=[DataRequired()])
    account_name = StringField(
        label='Nama Pemilik Rekening', validators=[DataRequired()])
    submit = SubmitField(label='Daftar')

class RegisterBorrowerForm(FlaskForm):

    # Function to catch input error
    # The name validate_[field] is the convention in Flask, so FlaskForm understand this
    # validation is for username
    def validate_username(self, username_to_check):
        user = Borrower.query.filter_by(username=username_to_check.data).first()
        if(user):
            raise ValidationError('Username telah digunakan')

    def validate_email(self, email_to_check):
        email = Borrower.query.filter_by(email=email_to_check.data).first()
        if(email):
            raise ValidationError('Email ini telah digunakan')

    username = StringField(label='User Name', validators=[
                           Length(min=2, max=30), DataRequired()])
    email = StringField(label='Email', validators=[
                        Email(), DataRequired()])
    password1 = PasswordField(label='Password', validators=[
                              Length(min=6), DataRequired()])
    password2 = PasswordField(label='Konfirmasi Password', validators=[
                              EqualTo('password1'), DataRequired()])
    phone_number = StringField(label='Kontak Telepon', validators=[
        Length(min=11, max=13), DataRequired()])
    fullname = StringField(label='Nama Lengkap', validators=[
                           Length(min=2, max=100), DataRequired()])                      
    birth_place = StringField(label='Tempat Lahir', validators=[
        DataRequired()])
    birth_date = DateField('Tanggal Lahir', format='%Y-%m-%d', validators=[
        DataRequired()])
    gender = RadioField(label='Jenis Kelamin', choices=['Laki-Laki', 'Perempuan'], validators=[
        DataRequired()])
    submit = SubmitField(label='Daftar')


class LoginForm(FlaskForm):
    username = StringField(label='User Name', validators=[DataRequired()])
    password = PasswordField(label='Password', validators=[DataRequired()])
    submit = SubmitField(label='Masuk')
