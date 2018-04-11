import api
from flask import jsonify
from api.business import get_college_by_name, get_department_by_name, get_program_by_name, \
    get_courses, get_general_course_by_name, get_specific_course_by_name


app = api.app


@app.route('/colleges/<college_name>', methods=['GET'])
def get_colleges(college_name):
    return jsonify({"college": get_college_by_name(college_name)})


@app.route('/departments/<department_name>', methods=['GET'])
def get_departments(department_name):
    return jsonify({"department": get_department_by_name(department_name)})


@app.route('/programs/<program_name>', methods=['GET'])
def get_programs(program_name):
    return jsonify({"program": get_program_by_name(program_name)})


@app.route('/courses/', methods=['GET'])
def get_courses(course_name):
    return jsonify({"courses": get_courses()})


@app.route('/generalcourses/<course_name>', methods = ["GET"])
def get_general_courses(course_name):
    return jsonify({"general_courses": get_general_course_by_name(course_name)})


@app.route('/specificcourses/<course_name>', methods = ["GET"])
def get_specific_courses(course_name):
    return jsonify({"specific_courses": get_specific_course_by_name(course_name)})
