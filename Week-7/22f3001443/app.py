import os
from flask import Flask
from flask import render_template
from flask import request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy


# Course Data Dictionary
cdd = {
    'course_1' : 'MAD I',
    'course_2' : 'DBMS',
    'course_3' : 'PDSA',
    'course_4' : 'BDM'
}


# SETTING APP AND DATABASE
current_dir = os.path.abspath(os.path.dirname(__file__))

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///" + os.path.join(current_dir, "week7_database.sqlite3")

db = SQLAlchemy()
db.init_app(app)
app.app_context().push()



# MODELS
class Student(db.Model):
    __tablename__ = 'student'
    student_id  = db.Column(db.Integer, autoincrement=True, primary_key=True)
    roll_number = db.Column(db.String, unique=True)
    first_name = db.Column(db.String)
    last_name = db.Column(db.String)
    courses = db.relationship('Enrollments', backref='student', lazy=True)

class Course(db.Model):
    __tablename__ = 'course'
    course_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    course_code = db.Column(db.String, unique=True)
    course_name = db.Column(db.String)
    course_description = db.Column(db.String)
    students = db.relationship('Enrollments', backref='course', lazy=True)

class Enrollments(db.Model):
    __tablename__ = 'enrollments'
    enrollment_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    estudent_id = db.Column(db.Integer, db.ForeignKey("student.student_id"), nullable=False)
    ecourse_id = db.Column(db.Integer, db.ForeignKey("course.course_id"), nullable=False)



# CONTROLLERS
@app.route('/', methods=['POST', 'GET'])
def home():
    students = Student.query.all()
    return render_template('home.html', students=students)


@app.route('/student/create', methods=['GET', 'POST'])
def create():
    if request.method == 'GET':
        return render_template('create.html')
    else:
        form = request.form
        first_name = form.get('f_name')
        last_name = form.get('l_name')
        roll_number = form.get('roll')


        # Check if roll_number already exists
        roll_numbers = db.session.query(Student.roll_number).all()
        roll_number_list = [row[0] for row in roll_numbers]
        if roll_number in roll_number_list:
            return "Student already exists. Please use different Roll Number!<br><a href='/'>Go Home</a>"



        # Student object
        new_student = Student(
            first_name=first_name,
            last_name=last_name,
            roll_number=roll_number
        )
        db.session.add(new_student)
        db.session.commit()


        return redirect(url_for('home'))


@app.route('/student/<int:student_id>/update', methods=['GET', 'POST'])
def update(student_id):
    if request.method == 'GET':
        student = Student.query.filter_by(student_id = student_id).first()        

        return render_template('update.html', student=student)


    else:
        form = request.form
        first_name = form.get('f_name')
        last_name = form.get('l_name')
        course_id = form.get('course')

        student = Student.query.filter_by(student_id=student_id).first()

        # Update student information
        student.first_name = first_name
        student.last_name = last_name

        # Add new enrollment
        enrollment = Enrollments(estudent_id=student_id, ecourse_id=course_id)
        db.session.add(enrollment)

        # Commit the changes to the database
        db.session.commit()

        # return student.roll_number
        return redirect(url_for('home'))



@app.route('/student/<int:student_id>/delete', methods=['GET'])
def delete(student_id):
    Enrollments.query.filter_by(estudent_id=student_id).delete()
    Student.query.filter_by(student_id=student_id).delete()
    db.session.commit()
    return redirect(url_for('home'))


@app.route('/student/<int:student_id>')
def student(student_id):
    student = Student.query.filter_by(student_id=student_id).first()

    course_ids = Enrollments.query.add_columns(Enrollments.ecourse_id).filter_by(estudent_id=student_id).all()
    course_id_list = [row[0].ecourse_id for row in course_ids]
    courses = Course.query.filter(Course.course_id.in_(course_id_list)).all()

    return render_template('student.html', student=student, courses=courses)


@app.route('/student/<int:student_id>/withdraw/<int:course_id>')
def withdraw(student_id, course_id):
    enrollment = Enrollments.query.filter_by(estudent_id=student_id, ecourse_id=course_id).first()
    db.session.delete(enrollment)
    db.session.commit()
    return redirect(url_for('home'))

@app.route('/courses')
def courses():
    courses = Course.query.all()
    return render_template('courses.html', courses=courses)


@app.route('/course/create', methods=['POST', 'GET'])
def create_course():
    if request.method == 'GET':
        return render_template('create_course.html')
    else:
        data = request.form
        course_code = data.get('code')
        course_name = data.get('c_name')
        course_description = data.get('desc')

        # Course already exists
        courses = db.session.query(Course.course_code).all()
        course_list = [row[0] for row in courses]
        if course_code in course_list:
            return "Course already exists. Please use different Course!<br><a href='/courses'>Go Home</a>"

        course = Course(
            course_code = course_code,
            course_name = course_name,
            course_description = course_description
        )

        db.session.add(course)
        db.session.commit()
        return redirect(url_for('courses'))


@app.route('/course/<int:course_id>/update', methods=['POST', 'GET'])
def course_update(course_id):
    if request.method == 'GET':
        course = Course.query.filter_by(course_id=course_id).first()
        return render_template('course_update.html', course=course)
    else:
        data = request.form
        course_name = data.get('c_name')
        course_description = data.get('desc')

        course = Course.query.filter_by(course_id=course_id).first()
        course.course_name = course_name
        course.course_description = course_description

        db.session.commit()

        return redirect(url_for('courses'))

@app.route('/course/<int:course_id>/delete', methods=['GET'])
def course_delete(course_id):
    Course.query.filter_by(course_id=course_id).delete()
    db.session.commit()
    return redirect(url_for('home'))


@app.route('/course/<int:course_id>')
def course(course_id):
    course = Course.query.filter_by(course_id=course_id).first()
    students = course.students
    student_ids = [row.estudent_id for row in students]
    students = Student.query.filter(Student.student_id.in_(student_ids)).all()

    return render_template('course.html', students=students, course=course)


if __name__ == '__main__':
    app.run(debug=True)