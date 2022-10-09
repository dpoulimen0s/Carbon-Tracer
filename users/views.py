import logging
import os
from flask import Blueprint, render_template, flash, redirect, url_for, session, request
from flask_login import login_user, logout_user, current_user, login_required
from werkzeug.security import check_password_hash
from sqlalchemy import desc

from app import db
from models import User, Message, Emission
from users.forms import RegisterForm, LoginForm, MessageForm

users_blueprint = Blueprint('users', __name__, template_folder='templates')


@users_blueprint.route('/register', methods=['GET', 'POST'])
def register():
    '''After filling all the fields a user i created and then notifying the user that
    a user has been created'''
    form = RegisterForm()

    if form.validate_on_submit():

        user = User.query.filter_by(username=form.username.data).first()

        if user:
            flash('Username already exists', "danger")
            return render_template('users/register.html', form=form)

        new_user = User(
            firstname=form.firstname.data,
            lastname=form.lastname.data,
            username=form.username.data,
            email=form.email.data,
            password=form.password.data,
            role='user',
            update=True)

        db.session.add(new_user)
        db.session.commit()

        new_message = Message(sender='admin',
                              receiver=form.username.data,
                              header="Welcome to Carbon Tracer!",
                              body="To " + form.firstname.data +
                                   ", \nI am delighted to welcome you to the Carbon "
                                   "Tracer family!! Why not give our Quiz and Carbon "
                                   "Calculator a try now!",
                              read=False)
        db.session.add(new_message)
        db.session.commit()

        # Send new user registered notification to security log file
        logging.warning('SECURITY - User registration [%s, %s]',
                        form.email.data, request.remote_addr)

        # Sends user to login page and displays a message that a user has been created.
        return redirect(url_for('users.login')), \
               flash('The user ' + new_user.email + ' has been created!', "success")

    return render_template('users/register.html', form=form)


@users_blueprint.route('/login', methods=['GET', 'POST'])
def login():
    '''After filling the two fields for login it checks them, if they are ok it redirects
    the user accordingly otherwise it displays the appropriate message'''
    # if session attribute logins does not exist create attribute logins
    if not session.get('logins'):
        session['logins'] = 0
    # if login attempts is 3 or more create an error message
    elif session.get('logins') >= 3:
        flash('Number of incorrect logins exceeded', "warning")

    form = LoginForm()

    if form.validate_on_submit():

        # increase login attempts by 1
        session['logins'] += 1

        user = User.query.filter_by(username=form.username.data).first()

        if not user or not check_password_hash(user.password, form.password.data):
            # if no match create appropriate error message based on login attempts
            if session['logins'] == 3:
                flash('Number of incorrect logins exceeded', "warning")

            elif session['logins'] == 2:
                flash('Please check your login details and try again.'
                      ' 1 login attempt remaining', "warning")

            else:
                flash('Please check your login details and try again.'
                      ' 2 login attempts remaining', "warning")

                # Send Invalid log in attempt notification to security log file
                logging.warning('SECURITY - Invalid log in attempt [%s, %s]', form.username.data, request.remote_addr)

            return render_template('users/login.html', form=form)

        session['logins'] = 0

        login_user(user)

        db.session.commit()

        # Send Log in notification to security log file
        logging.warning('SECURITY - Log in [%s, %s, %s]',
                        current_user.id, current_user.email, request.remote_addr)

        return redirect(url_for('users.profile'))

    return render_template('users/login.html', form=form)


@users_blueprint.route('/logout')
def logout():
    '''Logouts the current logged in user'''
    # Send Log out notification to security log file
    logging.warning('SECURITY - Log out [%s, %s, %s]',
                    current_user.id, current_user.email, request.remote_addr)

    logout_user()
    return redirect(url_for('index'))


# Author: Zhuolin Yong (Winter)
# View user profile
@users_blueprint.route('/profile', methods=["POST", "GET"])
@login_required
def profile():
    '''Updates the fields of the current user'''
    if request.method == 'GET':
        pic_exist = False
        from app import APP_DIR
        if (os.path.exists(os.path.join(os.path.join(APP_DIR, "static\\img\\users\\%s.jpg" % current_user.username)))):
            pic_exist = True
        return render_template('users/profile.html', pic_exist=pic_exist)
    else:
        firstname = request.form.get('firstname')
        lastname = request.form.get('lastname')
        email = request.form.get('email')
        pass1 = request.form.get('pass1')
        pass2 = request.form.get('pass2')
        file = request.files['file']
        print(firstname, lastname, email, pass1, pass2, file)

        cur_username = current_user.username
        print(cur_username)
        user = User.query.filter_by(username=cur_username).first()
        print(user)
        if firstname:
            current_user.firstname = firstname
            user.firstname = firstname
            db.session.commit()
        if lastname:
            current_user.lastname = lastname
            user.lastname = lastname
            db.session.commit()
        if email:
            current_user.email = email
            user.email = email
            db.session.commit()
        if pass1 and pass2:
            from wtforms import PasswordField
            if str(pass1) == str(pass2):
                from werkzeug.security import generate_password_hash
                current_user.password = generate_password_hash(pass1)
                user.password = generate_password_hash(pass1)
                db.session.commit()
            else:
                flash("Password fields are not equal")
                

        pic_exist = False
        from app import APP_DIR
        if os.path.exists(os.path.join(os.path.join(APP_DIR, "static\\img\\users\\%s.jpg" % current_user.username))):
            pic_exist = True
        return render_template('users/profile.html', pic_exist=pic_exist)


# Author: Dimitrios Poulimenos
@users_blueprint.route('/panel')
@login_required
def panel():
    '''It displays the panel of the user and rendering results accordingly'''
    emissions = Emission.query.order_by('result').all()
    for emission in emissions:
        emission.rank = emissions.index(emission) + 1
    return render_template('users/panel.html',
                           emissions=Emission.query.filter_by(username=current_user.username).all(),
                           emissions2=Emission.query.order_by('result').all())


# Author: William Newbould
# View Inbox and all messages contained within it
@users_blueprint.route('/inbox', methods=['GET', 'POST'])
@login_required
def inbox():
    '''  '''
    form = MessageForm()

    # variable used to check for the automated update header, this value is done in inbox.html
    quizupdate = "New questions have been added to our quiz!"

    # sends message from current user to user specified in the form
    if form.validate_on_submit():
        new_message = Message(sender=current_user.username,
                              receiver=form.receiver.data,
                              header=form.header.data,
                              body=form.body.data,
                              read=False)
        db.session.add(new_message)
        db.session.commit()

    # read messages for a given user are found by looking for messages sent to that user and where read = true
    read = Message.query.filter_by(receiver=current_user.username, read=True).order_by(desc('date')).all()

    # unread messages for a given user are found by looking for messages sent to that user and where read = false
    unread = Message.query.filter_by(receiver=current_user.username, read=False).order_by(desc('date')).all()

    # initialise variable to store number of messages in each category
    unread_total = 0
    read_total = 0
    older_total = 0

    # adds 1 to the message total for every message in the unread list
    for message in unread:
        unread_total += 1

    # adds 1 to the message total for every message in the unread list
    for message in read:
        read_total += 1

    # this value is used to limit both the read and unread categories to just display the latest 5 messages
    # the older category holds all read message outside of that 5 limit
    inbox_limit = 5

    older = read[inbox_limit:]
    read = read[:inbox_limit]
    unread = unread[:inbox_limit]

    # adds 1 to the message total for every message in the older list
    for message in older:
        older_total += 1

    return render_template('inbox.html', form=form,
                           read=read,
                           users=User.query.all(),
                           unread=unread,
                           older=older,
                           read_total=read_total,
                           unread_total=unread_total,
                           older_total=older_total,
                           quizUpdate=quizupdate)


# Author: Will Newbould
# Change status of message from un-read to read
@users_blueprint.route('/read/<id>')
@login_required
def read(id):
    '''Takes the id of a message and changes status of that message from un-read to read'''
    read = Message.query.filter_by(id=int(id)).first()
    read.read = True
    db.session.commit()

    return redirect(url_for('users.inbox'))


# Author: Will Newbould
# Change status of all unread messages from un-read to read
@users_blueprint.route('/readAll')
@login_required
def read_all():
    '''Changes every message from unread to read'''
    read = Message.query.filter_by(receiver=current_user.username, read=False).all()
    for message in read:
        message.read = True
        db.session.commit()

    return redirect(url_for('users.inbox'))


# Author: Will Newbould
# Change status of message from read to un-read
@users_blueprint.route('/unread/<id>')
@login_required
def unread(id):
    '''Change status of message from read to un-read'''
    unread = Message.query.filter_by(id=int(id)).first()
    unread.read = False
    db.session.commit()

    return redirect(url_for('users.inbox'))


# Author: Will Newbould
# Delete any given message
@users_blueprint.route('/delete_message/<id>')
@login_required
def delete(id):
    '''Delete any given message'''
    Message.query.filter_by(id=int(id)).delete()
    db.session.commit()

    return redirect(url_for('users.inbox'))


# Author: Will Newbould
# Delete all messages in the 'older' section
@users_blueprint.route('/delete_older_messages')
@login_required
def delete_all_older():
    '''Delete all messages in the 'older' section'''
    # Find read messages directed to the current user and order by date (newest at the top)
    read = Message.query.filter_by(receiver=current_user.username, read=True).order_by(desc('date')).all()

    # variable that limits the number of visible messages in the read and unread sections
    inbox_limit = 5

    # Older displays all the read messages that do not fit in the read section
    # Creates a list and stores all values that do not fit in the read section
    older = read[inbox_limit:]

    # delete each message in the older selection
    for message in older:
        Message.query.filter_by(id=message.id).delete()
        db.session.commit()

    return redirect(url_for('users.inbox'))


# Author: Will Newbould
# Change update preference regarding receiving updates when new questions are added to the quiz
@login_required
@users_blueprint.route('/update_preferences')
def update_preferences():
    '''Change update preference regarding receiving updates when new questions are added to the quiz'''
    # Find the current user in the database
    user = User.query.filter_by(username=current_user.username).first()
    # If their update preference is False (off) then this method changes it to True (on)
    if not user.update:
        user.update = True
        db.session.commit()
    # If their update preference is True (on) then this method changes it to False (off)
    else:
        user.update = False
        db.session.commit()

    return redirect(url_for('users.inbox'))
