from flask import Blueprint, render_template, request, flash, current_app, redirect, url_for
# from flask_login import login_required, current_user
# from flask_security import roles_required
# from werkzeug.utils import secure_filename
# from datetime import datetime, date
import time
import os
import random
from . import db
from .models import Question, slugify

views = Blueprint("views", __name__)

ROWS_PER_PAGE = 10

# def time_convert(sec):
#     mins = sec // 60
#     sec = sec % 60
#     hours = mins // 60
#     mins = mins % 60
#     print("Time Lapsed = {0}:{1}:{2}".format(int(hours), int(mins), sec))


@views.errorhandler(404)
def not_found(e):
    return render_template('404.html')


@views.route('/')
def home():
    return render_template("home.html")


# Query and display 3 random questions from database
@views.route('/questions', methods=['GET', 'POST'])
def query_questions():
    global questions
    global query_result
    query = Question.query.all()

    if 'quit' in request.form:
        return render_template('home.html')

    elif request.form and query_result:
        for x in query_result:
            questions.remove(x)

    elif 'next' in request.form or not request.form:
        if not request.form:
            questions = query

    try:
        quiz = random.sample(questions, 3)
    except ValueError:
        flash('W bazie danych jest za mało pytań', category='error')
        return redirect(url_for('views.home'))
    query_result = quiz
    return render_template('questions/query_questions.html', questions=quiz)

    # input("Press Enter to start")
    # start_time = time.time()
    # input("Press Enter to stop")
    # end_time = time.time()
    # time_lapsed = end_time - start_time
    # time_convert(time_lapsed)


@views.route('/create-question', methods=['GET', 'POST'])
def create_question():
    if request.method == 'POST':
        title = request.form.get("title")
        # content = request.form.get("content")
        content = request.form.get("ckeditor")
        if not title or not content:
            flash('Please fill in all the fields.', category='error')
        else:
            new_phrase = Question(title=title, content=content)
            db.session.add(new_phrase)
            db.session.commit()
            flash('Phrase created!', category='success')
            # return redirect(url_for('views.admin_console'))
    return render_template('questions/create_question.html')


@views.route('/edit-question/<slug>', methods=['GET', 'POST'])
def edit_question(slug):

    question = Question.query.filter(Question.slug == slug).first()

    if request.method == 'POST':
        title = request.form.get("title")
        content = request.form.get("ckeditor")

        if question.title != title:
            question.title = title
            question.slug = slugify(title)

        question.content = content
        db.session.add(question)
        db.session.commit()

        flash('Zmiany zostały zapisane!', category='success')
        return redirect(url_for('views.show_all_questions'))

    return render_template('questions/edit_question.html', question=question)


@views.route('/show-question/<slug>')
def show_question(slug):
    question = Question.query.filter(Question.slug == slug).first()
    return render_template('questions/show_question.html', question=question)


@views.route('/show-all-questions')
def show_all_questions():
    page = request.args.get('page', 1, type=int)
    questions = Question.query.paginate(page=page, per_page=ROWS_PER_PAGE)

    return render_template('questions/show_questions.html', questions=questions)


@views.route('/delete-question/<slug>')
def delete_question(slug):
    pass
