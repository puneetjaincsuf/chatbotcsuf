import models
import api
from flask import jsonify, request
import logging

app = api.app


@app.route('/colleges', methods=['GET'])
def get_colleges():

    """
    Query the college table in database

    :return: Colleges data
    """
    try:
        data = models.College.query.all()
        college_schema = models.CollegeSchema(many=True)
        colleges = college_schema.dump(data).data
        logging.debug(colleges)
        return jsonify({"college": colleges})
    except (RuntimeError, TypeError, NameError) as err:
        logging.warning("Error Occurred: {0}".format(err))
    except ValueError as verr:
        print("Value Error Occurred: {0}".format(verr))
    except:
        print("Unexpected error:")
        raise


@app.route('/departments', methods=['GET'])
def get_departments():

    """
    Query the department table in database

    :return: Departments data
    """
    try:
        data = models.Department.query.all()
        department_schema = models.DepartmentSchema(many=True)
        department = department_schema.dump(data).data
        logging.debug(department)
        return jsonify({"department": department})
    except (RuntimeError, TypeError, NameError) as err:
        logging.warning("Error Occurred: {0}".format(err))
    except ValueError as verr:
        print("Value Error Occurred: {0}".format(verr))
    except:
        print("Unexpected error:")
        raise


@app.route('/programs', methods=['GET'])
def get_programs():

    """
    Query the program table in database

    :return: Programs data
    """
    try:
        data = models.Program.query.all()
        program_schema = models.ProgramSchema(many=True)
        program = program_schema.dump(data).data
        logging.debug(program)
        return jsonify({"program": program})
    except (RuntimeError, TypeError, NameError) as err:
        logging.warning("Error Occurred: {0}".format(err))
    except ValueError as verr:
        print("Value Error Occurred: {0}".format(verr))
    except:
        print("Unexpected error:")
        raise

@app.route('/courses', methods=['GET'])
def get_courses(course_name):

    """
    Query the course table in database

    :return: Courses data
    """
    try:
        data = models.Course.query.all()
        course_schema = models.CourseSchema(many=True)
        course = course_schema.dump(data).data
        logging.debug(course)
        return jsonify({"courses": course})
    except (RuntimeError, TypeError, NameError) as err:
        logging.warning("Error Occurred: {0}".format(err))
    except ValueError as verr:
        print("Value Error Occurred: {0}".format(verr))
    except:
        print("Unexpected error:")
        raise

@app.route('/generalcourses/<course_name>', methods = ["GET"])
def get_general_courses(course_name):

    """
    Query the general table in database

    :return: General courses data
    """
    try:
        #data = models.General.query.all()
        data = models.General.query.filter(models.General.name == course_name).first( )
        general_course_schema = models.GeneralSchema(many=True)
        general_course = general_course_schema.dump(data).data
        logging.debug(general_course)
        return jsonify({"general courses": general_course})
    except (RuntimeError, TypeError, NameError) as err:
        logging.warning("Error Occurred: {0}".format(err))
    except ValueError as verr:
        print("Value Error Occurred: {0}".format(verr))
    except:
        print("Unexpected error:")
        raise

@app.route('/specificcourses/<course_name>', methods = ["GET"])
def get_specific_courses(course_name):

    """
    Query the specific table in the database

    :return: Specific courses data
    """
    try:
        data = models.Specific.query.all()
        specific_course_schema = models.SpecificSchema(many=True)
        specific_course = specific_course_schema.dump(data).data
        logging.debug(specific_course)
        return jsonify({"specific courses": specific_course})
    except (RuntimeError, TypeError, NameError) as err:
        logging.warning("Error Occurred: {0}".format(err))
    except ValueError as verr:
        print("Value Error Occurred: {0}".format(verr))
    except:
        print("Unexpected error:")
        raise