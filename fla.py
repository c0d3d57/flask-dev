#!/usr/bin/env python

from wtforms import TextField, PasswordField, validators, HiddenField, TextAreaField, BooleanField
from wtforms.validators import DataRequired, Required, EqualTo, Optional, Length, Email
from flask import render_template, request, flash, url_for, redirect, session
from flask.ext.login import LoginManager, login_required, login_user, logout_user, current_user
from sqlalchemy import or_, and_
from flask.ext.wtf import Form
import re

from conf import app
from models import db, Login, Comment


login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'signin'


@login_manager.user_loader
def user_loader(userid):
	return Login.query.filter_by(email=userid).first()



class SigninForm(Form):
	password = PasswordField('Pick a secure password', validators=[
	DataRequired(),
	Length(min=5, message=(u'Please give a longer password'))])
	username = TextField('Choose your username', validators=[DataRequired()])

class SignupForm(Form):
	email = TextField('Email address', validators=[DataRequired('Please provide a valid email address'),
													Length(min=6, message=(u'Email address too short')),
	Email(message=(u'That\'s not a valid email address.'))])
	password = PasswordField('Pick a secure password', validators=[DataRequired(),Length(min=5, message=(u'Please give a longer password'))])
	username = TextField('Choose your username', validators=[DataRequired()])
	agree = BooleanField('I agree all your Terms of Services',validators=[Required(u'You must accept our Terms of Service')])

class ContactForm(Form):
	email = TextField('Email address', validators=[
	DataRequired('Please provide a valid email address'),
	Length(min=6, message=(u'Email address too short')),
	Email(message=(u'That\'s not a valid email address.'))])
	fullname = TextField('Enter a name', validators=[DataRequired()])
	phone = TextField('Phone: (Optional)')
	subject = TextField('Subject', validators=[DataRequired()])
	message = TextField('Message', validators=[DataRequired()])

class CommentForm(Form):
	fullname = TextField('Enter a name', validators=[DataRequired()])
	message = TextField('Message', validators=[DataRequired()])

@app.route('/index/')
@app.route('/index/<name>')
def index(name = None):
	if name is None:
		return '<html>This is my first<h1>Hello World!</h1><br>Message in different <b>STYLES</b> So...Yea, lets get started!<html>'
	else:
		return '<html>This is my first<h1>Hello %s</h1><br>Message in different <b>STYLES</b> So...Yea, lets get started!<html>' % name


@app.route('/signup/', methods=['GET', 'POST'])
def signup():
	user = current_user
	form = SignupForm(request.form)
	if request.method == 'POST':
		usersid = form.username.data
		passs = form.password.data
		emailadd = form.email.data

		if not usersid or not passs:
			flash('all fields required')
			return render_template('register.html', form = form, user = user)

		if re.match(r"^[a-zA-Z0-9._]+\@[a-zA-Z0-9._]+\.[a-zA-Z]{3,}$", emailadd) == None:
			flash("Wrong E-mail Format")
			return render_template('register.html', form = form, user = user)

		users = Login.query.filter(or_(Login.username==usersid,Login.email==emailadd)).first()
		if users:
			flash("User already registered")
			return redirect(url_for('signup'))
		else:
			register = Login(usersid, passs, emailadd)
			db.session.add(register)
			db.session.commit()
			return render_template('register.html', form = form, keyword = 'Successfull', user = user)
	return render_template('register.html', form = SignupForm(), user = user)


@app.route('/signin/', methods=['GET', 'POST'])
def signin():
	if current_user.is_active():
		return redirect(url_for('welcome'))

	form = SigninForm(request.form)
	if request.method == 'POST':
		userid = form.username.data
		passwd = form.password.data

		users = Login.query.filter(and_(Login.username==userid,Login.password==passwd)).first()
		if not users:
			flash("Invalid Login Attempt")
			return redirect(url_for('signin'))
		else:
			login_user(users)
			return redirect(url_for('welcome'))
			#return render_template('welcome.html', form = form)
	return render_template('login.html', form = SigninForm())

@app.route('/logout/')
@login_required
def logout():
	logout_user()
	return render_template('logout.html')


@app.route('/contact/', methods=['GET', 'POST'])
def contact():
	user = current_user
	form = ContactForm(request.form)
	if request.method == 'POST':
		name = form.fullname.data
		phone = form.phone.data
		email = form.email.data
		mbody = form.message.data
		subje = form.subject.data

		try:
			if not name and not subje:
				raise ValueError('Empty Space')
		except:
			ValueError
			return render_template('contact.html', form = form, keyword = 'Please provide a name, email and subject address', user = user)

		if re.match(r"^[a-zA-Z0-9._]+\@[a-zA-Z0-9._]+\.[a-zA-Z]{3,}$", email) == None:
			return render_template('contact.html', form = form, keyword = 'Wrong E-mail Format', user = user)
	return render_template('contact.html', form = ContactForm(), user = user)

	
@app.route('/comments/', methods=['GET', 'POST'])
def comments():
	user = current_user
	form = CommentForm(request.form)
	post = Comment.query.all()
	if request.method == 'POST':
		name = form.fullname.data
		mbody = form.message.data

		if not name and not mbody:
			flash('Empty Space')
			return redirect(url_for('comments'))
		else:
			comment = Comment(name, mbody)
			db.session.add(comment)
			db.session.commit()
			flash('Thank You')
			return redirect(url_for('comments'))
	return render_template('comments.html', form = CommentForm(), post = post)

# @app.route('/comments2/')
# def comments2():
# 	post = Comment.query.all()
# 	return render_template('comments2.html', post = post)


@app.route('/welcome/')
@login_required
def welcome():
	user = current_user
	return render_template('welcome.html', user = user)

@app.route('/product/')
@login_required
def product():
	user = current_user
	return render_template('product.html', user = user)

@app.route('/aboutus/')
def aboutus():
	user = current_user
	return render_template('about.html', user = user)

@app.route('/home/')
def home():
	user = current_user
	return render_template('index.html', user = user)

@app.route('/technology/')
def technology():
	user = current_user
	return render_template('technology.html', user = user)


if __name__ == '__main__':
	app.run(debug=True)