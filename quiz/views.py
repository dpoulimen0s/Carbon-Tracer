# Imports
import copy
from flask import Blueprint, render_template
from models import User, Quiz


# Config
quiz_blueprint = Blueprint('quiz', __name__, template_folder='templates')


# Author: William Newbould
# Displays the quiz and all the questions in the quiz database along with their selectable options
@quiz_blueprint.route('/quiz')
def quiz():
    '''Takes the users quiz , encrypting and then decrypting for the user'''
    total = 0

    # looks for questions ordered by id number
    questions = Quiz.query.order_by('id').all()

    # Creates a list of copied question objects which are independent of database
    question_copies = list(map(lambda x: copy.deepcopy(x), questions))

    # empty list for decrypted copied question objects
    decrypted_questions = []

    # decrypt each copied question object and add it to decrypted_questions array
    # question number is the index of the question + 1
    # total is the maximum possible score
    for question in question_copies:
        user = User.query.first()
        question.view_question(user.userkey)
        decrypted_questions.append(question)
        question.question_number = question_copies.index(question) + 1
        total += 1

    # number of questions is the number of questions in the quiz
    number_of_questions = len(decrypted_questions)

    return render_template('quiz/quiz.html',
                           questions=decrypted_questions,
                           total=total,
                           number_of_questions=number_of_questions)
