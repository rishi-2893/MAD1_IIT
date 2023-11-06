# -----------------IMPORTS-----------------------------
import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_restful import Resource, Api

from flask_cors import CORS

from flask_restful import Resource
from flask_restful import fields, marshal_with
from flask_restful import reqparse

from werkzeug.exceptions import HTTPException
from flask import make_response
import json




# ----------------------APP, API AND DB SETUP-----------------
app = Flask(__name__)
CORS(app)

current_dir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///" + os.path.join(current_dir, "api_database.sqlite3")

# app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///api_database.sqlite3'

api = Api(app)

db = SQLAlchemy()
db.init_app(app)

app.app_context().push()





# -----------------------------MODELS-----------------------------
class Student(db.Model):
    __tablename__ = 'student'
    student_id  = db.Column(db.Integer, autoincrement=True, primary_key=True)
    roll_number = db.Column(db.String, unique=True)
    first_name = db.Column(db.String)
    last_name = db.Column(db.String)

    # courses
    courses = db.relationship('Enrollments', backref='student', lazy=True)

class Course(db.Model):
    __tablename__ = 'course'
    course_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    course_code = db.Column(db.String, unique=True)
    course_name = db.Column(db.String)
    course_description = db.Column(db.String)

class Enrollments(db.Model):
    __tablename__ = 'enrollments'
    enrollment_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    student_id = db.Column(db.Integer, db.ForeignKey("student.student_id"), nullable=False)
    course_id = db.Column(db.Integer, db.ForeignKey("course.course_id"), nullable=False)






# ---------------------------UTILITIES-------------------------------

course_fields = {
    'course_id':   fields.Integer,
    'course_name':    fields.String,
    'course_code':    fields.String,
    'course_description': fields.String
}


student_fields = {
    'student_id':   fields.Integer,
    'roll_number':    fields.String,
    'first_name':    fields.String,
    'last_name': fields.String
}


enrollment_fields = {
    'enrollment_id':   fields.Integer,
    'student_id':    fields.Integer,
    'course_id':    fields.Integer,
}


course_parser = reqparse.RequestParser()
course_parser.add_argument('course_name')
course_parser.add_argument('course_code')
course_parser.add_argument('course_description')


student_parser = reqparse.RequestParser()
student_parser.add_argument('first_name')
student_parser.add_argument('last_name')
student_parser.add_argument('roll_number')

enrollment_parser = reqparse.RequestParser()
enrollment_parser.add_argument('course_id')


# -------------------------------HTTP EXCEPTIONS----------------------------

class CourseNotFoundError(HTTPException):
    def __init__(self, status_code):
        self.response = make_response('', status_code)


class InternalServerError(HTTPException):
    def __init__(self, status_code):
        self.response = make_response('', status_code)


class Error(HTTPException):
    def __init__(self, status_code):
        self.response = make_response('', status_code)


class CourseError(HTTPException):
    def __init__(self, status_code, error_code, error_message):
        data = { "error_code" : error_code, "error_message": error_message }
        self.response = make_response(json.dumps(data), status_code)


class StudentError(HTTPException):
    def __init__(self, status_code, error_code, error_message):
        data = { "error_code" : error_code, "error_message": error_message }
        self.response = make_response(json.dumps(data), status_code)


class EnrollmentError(HTTPException):
    def __init__(self, status_code, error_code, error_message):
        data = { "error_code" : error_code, "error_message": error_message }
        self.response = make_response(json.dumps(data), status_code)



# ---------------------------------API-------------------------------

class CourseAPI(Resource):
    
    @marshal_with(course_fields)
    def get(self, course_id):
        course = Course.query.filter_by(course_id=course_id).first()

        if course is None:
            raise CourseNotFoundError(status_code=404)
        elif course:
            return course
        else:
            raise InternalServerError(status_code=500)


    def put(self, course_id):
        course = Course.query.filter_by(course_id=course_id).first()
        args = course_parser.parse_args()
        course_code = args.get('course_code', None)
        course_name = args.get('course_name', None)
        course_description = args.get('course_description', None)


        # Validations
        if not course_name:
            raise CourseError(status_code=400, error_code='COURSE001', error_message='Course Name is required')
        if not course_code:
            raise CourseError(status_code=400, error_code='COURSE002', error_message='Course Code is required')
        if course is None:
            raise CourseNotFoundError(status_code=404)
        if course:
            course.course_code = course_code
            course.course_name = course_name
            course.course_description = course_description
            db.session.commit()
            res = make_response('', 200)
            return res
        else:
            InternalServerError(status_code=500)


    def delete(self, course_id):
        course = Course.query.filter_by(course_id=course_id).first()
        
        if course is None:
            raise CourseNotFoundError(status_code=404)
        elif course:
            db.session.delete(course)
            db.session.commit()
            res = make_response('', 200)
            return res
        else:
            raise InternalServerError(status_code=500)
        
    
    def post(self):
        args = course_parser.parse_args()
        course_code = args.get('course_code', None)
        course_name = args.get('course_name', None)
        course_description = args.get('course_description', None)

        if not course_name:
            raise CourseError(status_code=400, error_code='COURSE001', error_message='Course Name is required')
        if not course_code:
            raise CourseError(status_code=400, error_code='COURSE002', error_message='Course Code is required')
    

        course_codes = Course.query.add_columns(Course.course_code).all()
        course_code_list = [row[0].course_code for row in course_codes]
        if course_code in course_code_list:
            raise Error(status_code=409)
        
        
        course = Course(
            course_code = course_code,
            course_name = course_name,
            course_description = course_description
        )
        db.session.add(course)
        db.session.commit()
        res = make_response('', 201)
        return res

        raise InternalServerError(status_code=500)


class StudentAPI(Resource):
    
    @marshal_with(student_fields)
    def get(self, student_id):
        student = Student.query.filter_by(student_id=student_id).first()

        if student is None:
            raise Error(status_code=400)
        elif student:
            return student
        else:
            raise InternalServerError(status_code=500)
    

    def put(self, student_id):
        student = Student.query.filter_by(student_id=student_id).first()
        args = student_parser.parse_args()
        first_name = args.get('first_name', None)
        last_name = args.get('last_name', None)
        roll_number = args.get('roll_number', None)


        # Validations
        if not roll_number:
            raise CourseError(status_code=400, error_code='STUDENT001', error_message='Roll Number required')
        if not first_name:
            raise CourseError(status_code=400, error_code='STUDENT002', error_message='First Name is required')
        if student is None:
            raise Error(status_code=404)
        if student:
            student.first_name = first_name
            student.last_name = last_name
            student.roll_number = roll_number
            db.session.commit()
            res = make_response('', 200)
            return res
        else:
            InternalServerError(status_code=500)

    def delete(self, student_id):
        student = Student.query.filter_by(student_id=student_id).first()
        
        if student is None:
            raise Error(status_code=404)
        elif student:
            db.session.delete(student)
            db.session.commit()
            res = make_response('', 200)
            return res
        else:
            raise InternalServerError(status_code=500)
        
    def post(self):
        args = student_parser.parse_args()
        first_name = args.get('first_name', None)
        last_name = args.get('last_name', None)
        roll_number = args.get('roll_number', None)

        if not roll_number:
            raise CourseError(status_code=400, error_code='STUDENT001', error_message='Roll Number required')
        if not first_name:
            raise CourseError(status_code=400, error_code='STUDENT002', error_message='First Name is required')
    

        roll_numbers = Student.query.add_columns(Student.roll_number).all()
        roll_number_list = [row[0].roll_number for row in roll_numbers]
        if roll_number in roll_number_list:
            raise Error(status_code=409)
        
        
        student = Student(
            first_name = first_name,
            last_name = last_name,
            roll_number = roll_number
        )
        db.session.add(student)
        db.session.commit()
        res = make_response('', 201)
        return res

        raise InternalServerError(status_code=500)


class StudentDataAPI(Resource):

    @marshal_with(enrollment_fields)
    def get(self, student_id):
        
        student = Student.query.filter_by(student_id=student_id).first()
        
        if student is None:
            raise EnrollmentError(status_code=400,error_code='ENROLLMENT002', error_message='Student does not exist')
        
        enrollments = student.courses

        if enrollments is None:
            raise Error(status_code=404)
        elif enrollments:
            return enrollments
        else:
            raise InternalServerError(status_code=500)
        

    @marshal_with(enrollment_fields)
    def post(self, student_id):

        student = Student.query.filter_by(student_id=student_id).first()
        if student is None:
            raise Error(status_code=404)

        args = enrollment_parser.parse_args()
        course_id = int(args.get('course_id', None))


        course_ids = Course.query.add_columns(Course.course_id).all()
        course_id_list = [row[0].course_id for row in course_ids]

        if course_id not in course_id_list:
            raise EnrollmentError(status_code=400, error_code='ENROLLMENT001', error_message='Course does not exist')


        enrollment = Enrollments(
            student_id = student_id,
            course_id = course_id
        )

        db.session.add(enrollment)
        db.session.commit()

        return student.courses, 201
        
        
    def delete(self, student_id, course_id):
        student = Student.query.filter_by(student_id=student_id).first()

        if student is None:
            raise EnrollmentError(status_code=400,error_code='ENROLLMENT002', error_message='Student does not exist')
        

        course_ids = Course.query.add_columns(Course.course_id).all()
        course_id_list = [row[0].course_id for row in course_ids]
        if course_id not in course_id_list:
            raise EnrollmentError(status_code=400, error_code='ENROLLMENT001', error_message='Course does not exist')
        
        
        enrollments = student.courses
        enrolled_courses = [ enrollment.course_id for enrollment in enrollments]
        if course_id not in enrolled_courses:
            raise Error(status_code=404)  
        

        enrolled_course = Enrollments.query.filter_by(student_id = student_id, course_id = course_id).first()
        db.session.delete(enrolled_course)
        db.session.commit()
        res = make_response('', 200)
        return res




# ---------------------MAPPING CLASSES------------------------
api.add_resource(CourseAPI, "/api/course", "/api/course/<int:course_id>")

api.add_resource(StudentAPI, "/api/student", "/api/student/<int:student_id>")

api.add_resource(StudentDataAPI, "/api/student/<int:student_id>/course", "/api/student/<int:student_id>/course", "/api/student/<int:student_id>/course/<int:course_id>")





# --------------------RUN----------------------
if __name__ == '__main__':
    app.run(debug=False)