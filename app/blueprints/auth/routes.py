from flask import render_template, request, flash, redirect, url_for
from .forms import LoginForm, RegisterForm, EditProfileForm
import requests
from . import bp as auth
from app.models import User
from flask_login import login_user, login_required, logout_user, current_user

@auth.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if request.method == 'POST' and form.validate_on_submit():
        # LOGIN THE USER HERE
        email = form.email.data.lower()
        password = form.password.data
                                #colname = value
        u = User.query.filter_by(email=email).first()
        if u and u.check_hashed_password(password):
            #Login Success!!!!
            flash('Successfully Logged in', 'success')
            login_user(u)
            return redirect(url_for('app.index'))
       
        error_string = "Incorrect Email/Password Combo"
        return render_template('login.html.j2', loginerror=error_string, form=form)
    return render_template('login.html.j2', form=form)

@auth.route('/logout', methods=['GET'])
@login_required
def logout():
    logout_user()
    flash('Successfully Logged out', 'primary')
    return redirect(url_for("social.index"))


@auth.route('/register', methods=["GET","POST"])
def register():
    form = RegisterForm()
    if request.method == 'POST' and form.validate_on_submit():
        new_user_data = {
            "first_name" : form.first_name.data.title(),
            "last_name" : form.last_name.data.title(),
            "email": form.email.data.lower(),
            "password":form.password.data,
            "icon" : form.icon.data
        }

        # Create an Empty User Object to become our new user
        new_user_object = User()

        #build the user from the form data
        new_user_object.from_dict(new_user_data)

        # Save our new user to the database
        new_user_object.save()

        #flash user telling them they registered
        flash("Successfully Registered", "success")
        return redirect(url_for("auth.login"))

    return render_template('register.html.j2', form=form)

@auth.route('/edit_profile', methods=['GET','POST'])
@login_required
def edit_profile():
    form = EditProfileForm()
    if request.method == 'POST' and form.validate_on_submit():
        edited_user_data = {
            "first_name" : form.first_name.data.title(),
            "last_name" : form.last_name.data.title(),
            "email": form.email.data.lower(),
            "password":form.password.data,
            "icon" : form.icon.data
        }
        user = User.query.filter_by(email = edited_user_data["email"]).first()
        if user and user.email != current_user.email:
            flash('Email is already in use', 'danger')
            return redirect(url_for("auth.edit_profile"))
            
        current_user.from_dict(edited_user_data)
        current_user.save()
        flash("Profile Updated", "success")
        return redirect(url_for("social.index"))
    return render_template('register.html.j2',form=form)