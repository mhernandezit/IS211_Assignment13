""" Flask app using a database backend """

import uuid
import re
from flask import Flask, session, redirect, render_template, request, flash, url_for
from werkzeug.security import check_password_hash, generate_password_hash
from database import db_session, init_db
from models import Teacher, Student, Quiz, Grades, RegistrationForm
from flask_bootstrap import Bootstrap
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
from sqlalchemy.ext.declarative import declarative_base

engine = create_engine('sqlite:///schools.db', convert_unicode=True, echo=True)
db_session = scoped_session(sessionmaker(autocommit=False,
                                         autoflush=False,
                                         bind=engine))
Base = declarative_base()
Base.query = db_session.query_property()


app = Flask(__name__)
bootstrap = Bootstrap(app)
app.secret_key = uuid.uuid4().hex
student_roster = []
quiz_roster = []
init_db()


@app.teardown_appcontext
def shutdown_session(exception=None):
    db_session.remove()


@app.route('/',  methods=['GET'])
def home_pg():
    if 'logged_in' in session:
        return redirect('/dashboard')
    else:
        return render_template('auth/login.html')


@app.route('/dashboard',  methods=['GET'])
def dashboard():
    if 'logged_in' in session:
        return render_template('cms/dashboard.html',
                               student_roster=student_roster,
                               quiz_roster=quiz_roster)
    else:
        return redirect('/')


@app.route('/login',  methods=['GET', 'POST'])
def login():
    error = None
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        user = Teacher.query.filter(Teacher.username == username).first()

        if user is None:
            error = 'Incorrect username.'
        elif not check_password_hash(Teacher.password, password):
            error = 'Incorrect password.'

        if error is None:
            session.clear()
            session['logged_in'] = True
            session['user_id'] = user.teacher_id

            for row in Student.query.all():
                if row not in student_roster:
                    student_roster.append((row))

            for row in Quiz.query.all():
                if row not in quiz_roster:
                    quiz_roster.append((row))

            return redirect('/dashboard')

        flash(error)
        return render_template('auth/login.html', error=error)

    if request.method == 'GET':
        return redirect('/dashboard')


@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegistrationForm(request.form)
    if request.method == 'POST' and form.validate():
        user = Teacher(form.username.data,
                       form.password.data)
        db_session.add(user)
        flash('Thanks for registering')
        return redirect(url_for('login'))
    return render_template('auth/register.html', form=form)


@app.route('/student/add',  methods=['GET', 'POST'])
def addstudent():
    if 'logged_in' in session:
        if request.method == 'GET':
            return render_template('cms/add_student.html')
        elif request.method == 'POST':
            firstname = request.form['firstname']
            lastname = request.form['lastname']
            error = None

            if not firstname:
                error = 'First name is required.'
            elif not lastname:
                error = 'Last name is required.'

            if re.search(r'[!@#$%^&*(),.?":{}|<>]', firstname):
                error = "Invalid characters used. " \
                        "Please do not include special characters."
            elif re.search(r'[!@#$%^&*(),.?":{}|<>]', lastname):
                error = "Invalid characters used. " \
                        "Please do not include special characters."

            if error is None:
                if not Student.query.filter(Student.firstname == firstname,
                                            Student.lastname == lastname):
                    new_student = Student(firstname, lastname)
                    db_session.add(new_student)
                    db_session.commit()

                for row in Student.query.all():
                    student_roster.append((row))
                return redirect('/dashboard')

        flash(error)
        return render_template('school/add_student.html')
    else:
        return redirect('/')


@app.route('/quiz/add',  methods=['GET', 'POST'])
def addquiz():
    if 'logged_in' in session:
        if request.method == 'GET':
            return render_template('school/add_quiz.html')
        elif request.method == 'POST':
            subject = request.form['subject']
            num_of_questions = request.form['num_of_questions']
            quiz_date = request.form['date']
            error = None

            if not subject:
                error = 'Subject is required.'
            elif not num_of_questions:
                error = 'Number of questions is required.'
            elif not quiz_date:
                error = 'Quiz date is required.'

            if re.search(r'[!@#$%^&*(),.?":{}|<>]', subject):
                error = "Invalid characters used in Subject. " \
                        "Please do not include special characters."

            if error is None:
                new_quiz = Quiz(subject, num_of_questions, quiz_date)
                db_session.add(new_quiz)
                db_session.commit()

                quiz_roster.append([subject, num_of_questions, quiz_date])
                return redirect('/dashboard')

        flash(error)
        return render_template('school/add_quiz.html')
    else:
        return redirect('/')


@app.route('/student/<path:student_id>', methods=['GET'])
def viewstudent(student_id):
    if 'logged_in' in session:
        student_data = []
        student_name = []

        for result in Student.query.filter(Student.id == student_id):
            if result not in student_name:
                student_name.append((result))

        for result in Grades.query.all():
            if result not in student_data:
                student_data.append((result))

        return render_template('school/student.html',
                               student_id=student_id,
                               student_data=student_data,
                               student_name=student_name)


@app.route('/results/add', methods=['GET', 'POST'])
def add_score():
    if 'logged_in' in session and request.method == 'GET':
        student_id = []
        quiz_id = []

        for row in Student.query.all():
            if row not in student_id:
                student_id.append((row))

        for row in Quiz.query.all():
            if row not in quiz_id:
                quiz_id.append((row))

        return render_template('school/add_score.html',
                               student_ids=student_id,
                               quiz_ids=quiz_id)

    elif 'logged_in' in session and request.method == 'POST':
        student_id = request.form['studentID']
        quiz_id = request.form['quizID']
        score = request.form['score']
        message = None

        grade_exists = Grades.query.filter(Grades.studentid == student_id,
                                           Grades.quizid == quiz_id)

        if grade_exists is None:
            new_grade = Grades(student_id, quiz_id, score)
            db_session.add(new_grade)
            db_session.commit()
            message = "Quiz added successfully!"
        else:
            message = "Duplicate quiz for this student found."

        flash(message)

        return redirect('/results/add')

    else:
        return redirect('/')


if __name__ == '__main__':
    app.run(debug=1)
