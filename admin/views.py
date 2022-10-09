# Imports
import copy
from flask import Blueprint, render_template, flash, redirect, url_for
from flask_login import login_required, current_user
from sqlalchemy import desc
from models import User, Quiz, Message, Emission
from app import db, requires_roles
from admin.forms import QuestionForm


# CONFIG
admin_blueprint = Blueprint('admin', __name__, template_folder='templates')


# ROUTES

# Author: William Newbould
# Main admin route. Contains all the viewing functionality available to admin users
# (had to put it all in one method due to using tabs)
@admin_blueprint.route('/admin', methods=['POST', 'GET'])
@login_required
@requires_roles('admin')
def admin():
    '''Takes in a number n, returns the square of n'''
    questions = Quiz.query.order_by(desc('id')).all()
    # creates a list of copied question objects which are independent of database
    question_copies = list(map(lambda x: copy.deepcopy(x), questions))

    # empty list for decrypted copied question objects
    decrypted_questions = []

    # decrypt each copied question object and add it to decrypted_questions array
    for question in question_copies:
        user = User.query.filter_by(username=current_user.username).first()
        question.view_question(user.userkey)
        decrypted_questions.append(question)

    # order entries in Emission so entries with the lowest result are first
    emissions = Emission.query.order_by('result').all()
    # for each entry in Emission make its rank its position in the list emission + 1
    for emission in emissions:
        emission.rank = emissions.index(emission) + 1

    return render_template('admin/admin.html',
                           current_users=User.query.all(),
                           questions=decrypted_questions,
                           emissions2=Emission.query.order_by('result').all())


@admin_blueprint.route('/contact')
def contact():
    return render_template('admin/contact.html')


@admin_blueprint.route('/terms')
def terms():
    return render_template('admin/terms.html')


# Author: William Newbould
# Method is used to create a question and add/store it to the database so it can be used for the quiz
@admin_blueprint.route('/create_question', methods=['GET', 'POST'])
@login_required
@requires_roles('admin')
def create_question():
    ''' This function handles the creation of questions'''
    # create question form
    form = QuestionForm()

    # if request method is POST or form is valid
    if form.validate_on_submit():

        question = Quiz.query.filter_by(question=form.question.data).first()

        # if this returns a question, then the question already exists in the database
        # if question exists redirect user to the view questions page with error message
        # so user can try again
        if question:
            flash('Question already exists', "danger")
            return render_template('admin/create_question.html', form=form)

        # create a new question with the question data
        new_question = Quiz(username=current_user.username,
                            question=form.question.data,
                            answer=form.answer.data,
                            option1=form.option1.data,
                            option2=form.option2.data,
                            option3=form.option3.data,
                            option4=form.option4.data,
                            userkey=current_user.userkey)

        # add the new question to the database
        db.session.add(new_question)
        db.session.commit()

        users = User.query.all()

        # for each user if they have their update preference on, send the aumoated message updating them about new
        # content on the quiz page
        for user in users:
            if user.update:
                new_message = Message(sender=current_user.username,
                                      receiver=user.username,
                                      header="New questions have been added to our quiz!",
                                      body="To " + user.firstname +
                                           ", \nI am delighted to let you know that we have "
                                           "added to our brilliant quiz! Why not give it a go "
                                            "now!",
                                      read=False)
                db.session.add(new_message)
                db.session.commit()

        # sends user to view questions page
        return redirect(url_for('admin.admin'))
    # if request method is get or form not valid re-render create question page
    return render_template('admin/create_question.html', form=form)


# Author: William Newbould
# This function allows for the admin to edit any given question should they want to change an option or fix a typo.
@admin_blueprint.route('/<int:id>/update_question', methods=('GET', 'POST'))
@login_required
@requires_roles('admin')
def update_question(id):
    '''This function takes the ID of the question and then updates that specific question'''
    # looks for question using provided id
    # if it does not exist, returns error
    question = Quiz.query.filter_by(id=id).first()
    if not question:
        return render_template('errors/500.html')

    form = QuestionForm()

    # submits the new data to the database (replacing the old data for the question) and returns admin back to the admin
    # page
    if form.validate_on_submit():
        question.update_question(form.question.data,
                                 form.option1.data,
                                 form.option2.data,
                                 form.option3.data,
                                 form.option4.data,
                                 form.answer.data,
                                 current_user.userkey)
        return admin()

    # creates a copy of post object which is independent of database
    question_copy = copy.deepcopy(question)

    # decrypt copy of post object
    question_copy.view_question(current_user.userkey)

    # set update form with title and body of copied post objects
    form.question.data = question_copy.question
    form.option1.data = question_copy.option1
    form.option2.data = question_copy.option2
    form.option3.data = question_copy.option3
    form.option4.data = question_copy.option4
    form.answer.data = question_copy.answer

    return render_template('admin/update_question.html', form=form)


# Author: William Newbould
# This function allows a user to delete any given question
@admin_blueprint.route('/<int:id>/delete_question')
@login_required
@requires_roles('admin')
def delete_question(id):
    ''' This function takes the ID of the question and then deletes it '''
    # looks for question using the provided id and deletes it, before returning the admin to the admin page
    Quiz.query.filter_by(id=id).delete()
    db.session.commit()

    return redirect(url_for('admin.admin'))


# Author: William Newbould
# This function allows the admin to delete any given user
@admin_blueprint.route('/<int:id>/delete_user')
@login_required
@requires_roles('admin')
def delete_user(id):
    '''This function takes the ID of a user and deletes that specific user'''
    # looks for user using the provided id and deletes it, before returning the admin to the admin page
    User.query.filter_by(id=id).delete()
    db.session.commit()

    return redirect(url_for('admin.admin'))


# Author: William Newbould
# Resets the leaderboard by deleting all entries in the Emission database
@admin_blueprint.route('/reset_leaderboard')
@login_required
@requires_roles('admin')
def reset_leaderboard():
    '''This function resets the leaderboard of our web application.'''
    # looks for all entries in the emission database
    reset = Emission.query.all()

    # delete each entry in the emission database
    for r in reset:
        Emission.query.filter_by(id=r.id).delete()
        db.session.commit()

    return redirect(url_for('admin.admin'))


# Author: William Newbould
# This function deletes any given result from the emission database
@admin_blueprint.route('/<int:id>/delete_result')
@login_required
@requires_roles('admin')
def delete_result(id):
    '''This function deletes any given result from the emission database'''
    # Looks for emission using provided id and deletes it
    Emission.query.filter_by(id=id).delete()
    db.session.commit()

    return redirect(url_for('admin.admin'))
