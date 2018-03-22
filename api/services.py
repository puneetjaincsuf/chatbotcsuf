import models
import api
from api.business import create_college, create_department, create_program, create_general_course
from flask import jsonify, request
import logging

app = api.app

@app.route('/getcolleges', methods=['GET'])
def get_colleges():
    try:
        data = models.College.query.all()
        college_schema = models.CollegeSchema(many=True)
        colleges = college_schema.dump(data).data
        logging.warning('Getting Colleges')
        return jsonify({"college": colleges})
    except (RuntimeError, TypeError, NameError) as err:
        logging.warning("Error Occurred: {0}".format(err))
    except ValueError as verr:
        print("Value Error Occurred: {0}".format(verr))
    except:
        print("Unexpected error:")
        raise

@app.route('/getdepartments', methods=['GET'])
def get_departments():
    try:
        data = models.Department.query.all()
        department_schema = models.DepartmentSchema(many=True)
        department = department_schema.dump(data).data
        logging.warning('Getting Departments')
        return jsonify({"department": department})
    except (RuntimeError, TypeError, NameError) as err:
        logging.warning("Error Occurred: {0}".format(err))
    except ValueError as verr:
        print("Value Error Occurred: {0}".format(verr))
    except:
        print("Unexpected error:")
        raise

@app.route('/getprograms', methods=['GET'])
def get_programs():
    try:
        data = models.Program.query.all()
        program_schema = models.ProgramSchema(many=True)
        program = program_schema.dump(data).data
        logging.warning('Getting Programs')
        return jsonify({"program": program})
    except (RuntimeError, TypeError, NameError) as err:
        logging.warning("Error Occurred: {0}".format(err))
    except ValueError as verr:
        print("Value Error Occurred: {0}".format(verr))
    except:
        print("Unexpected error:")
        raise

@app.route('/getcourses', methods=['GET'])
def get_courses():
    try:
        data = models.Course.query.all()
        course_schema = models.CourseSchema(many=True   )
        course = course_schema.dump(data).data
        logging.warning('Getting Courses')
        #program = [cand.serialize() for cand in data]
        return jsonify({"courses": course})
    except (RuntimeError, TypeError, NameError) as err:
        logging.warning("Error Occurred: {0}".format(err))
    except ValueError as verr:
        print("Value Error Occurred: {0}".format(verr))
    except:
        print("Unexpected error:")
        raise

@app.route('/getgeneralcourses', methods=['GET'])
def get_general_courses():
    try:
        data = models.General.query.all()
        general_course_schema = models.GeneralSchema(many=True)
        general_course = general_course_schema.dump(data).data
        logging.warning('Getting General Courses')
        return jsonify({"general courses": general_course})
    except (RuntimeError, TypeError, NameError) as err:
        logging.warning("Error Occurred: {0}".format(err))
    except ValueError as verr:
        print("Value Error Occurred: {0}".format(verr))
    except:
        print("Unexpected error:")
        raise

@app.route('/getspecificcourses', methods=['GET'])
def get_specific_courses():
    try:
        data = models.Specific.query.all()
        specific_course_schema = models.SpecificSchema(many=True)
        specific_course = specific_course_schema.dump(data).data
        logging.warning('Getting Specific Courses')
        return jsonify({"specific courses": specific_course})
    except (RuntimeError, TypeError, NameError) as err:
        logging.warning("Error Occurred: {0}".format(err))
    except ValueError as verr:
        print("Value Error Occurred: {0}".format(verr))
    except:
        print("Unexpected error:")
        raise

@app.route('/addcollege', methods=['POST'])
def add_college():
    data = request.get_json()
    create_college(data)
    return jsonify({'result': 'Course Added'})

@app.route('/adddepartment', methods=['POST'])
def add_department():
    data = request.get_json()
    create_department(data)
    return jsonify({'result': 'Department Added'})

@app.route('/addprogram', methods=['POST'])
def add_program():
    data = request.get_json()
    create_program(data)
    return jsonify({'result': 'Program Added'})

@app.route('/addgeneralcourse', methods=['POST'])
def add_general_course():
    data = request.get_json()
    create_general_course(data)
    return jsonify({'result': 'General Course Added'})