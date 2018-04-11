import models
import logging
from sqlalchemy import or_


def get_college_by_name(college_name):
    """
    Query the college table in database by name

    :return: Colleges data
    """
    looking_for = '%{0}%'.format(college_name)
    data = models.College.query.filter(models.College.name.ilike(looking_for))
    college_schema = models.CollegeSchema(many=True)
    college = college_schema.dump(data).data
    logging.debug(college)
    return college


def get_department_by_name(department_name):
    """
    Query the department table in database by name

    :return: Colleges data
    """
    looking_for = '%{0}%'.format(department_name)
    data = models.Department.query.filter(models.Department.name.ilike(looking_for))
    department_schema = models.DepartmentSchema(many=True)
    department = department_schema.dump(data).data
    logging.debug(department)
    return department


def get_program_by_name(program_name):
    """
    Query the program table in database by name

    :return: Colleges data
    """
    looking_for = '%{0}%'.format(program_name)
    data = models.Program.query.filter(models.Program.name.ilike(looking_for))
    program_schema = models.ProgramSchema(many=True)
    program = program_schema.dump(data).data
    logging.debug(program)
    return program


def get_courses():
    """
    Query the course table in database

    :return: Courses data
    """
    data = models.Course.query.all()
    course_schema = models.CourseSchema(many=True)
    courses = course_schema.dump(data).data
    logging.debug(courses)
    return courses


def get_general_course_by_name(course_name):
    """
    Query the general table in database by name

    :return: General courses data
    """
    looking_for = '%{0}%'.format(course_name)
    data = models.General.query.filter(
        or_(models.General.name.ilike(looking_for), models.General.short_name.ilike(looking_for)))
    general_course_schema = models.GeneralSchema(many=True)
    general_course = general_course_schema.dump(data).data
    logging.debug(general_course)
    return general_course


def get_specific_course_by_name(course_name):
    """
     Query the specific table in the database by name

     :return: Specific courses data
     """
    looking_for = '%{0}%'.format(course_name)
    data = models.Specific.query.filter(
        or_(models.Specific.name.ilike(looking_for), models.Specific.short_name.ilike(looking_for)))
    specific_course_schema = models.SpecificSchema(many=True)
    specific_course = specific_course_schema.dump(data).data
    logging.debug(specific_course)
    return specific_course


'''

def create_college(data):
    name = data.get('name')
    short_name = data.get('short_name')
    college = models.College(name=name, short_name=short_name)
    db.session.add(college)
    db.session.commit()


def create_department(data):
    name = data.get('name')
    short_name = data.get('short_name')
    department_owner = data.get('college_id')
    college = models.College.query.filter(models.College.id == department_owner).one()
    department = models.Department(name=name, short_name=short_name, department_owner=college)
    db.session.add(department)
    db.session.commit()


def create_program(data):
    name = data.get('name')
    type = data.get('type')
    short_name = data.get('short_name')
    program_owner = data.get('program_owner')
    program = models.Program(name=name, type=type, short_name=short_name, program_owner=program_owner)
    db.session.add(program)
    db.session.commit()


def create_general_course(data):
    name = data.get('name')
    number = data.get('number')
    prerequisite = data.get('prerequisite')
    short_name = data.get('short_name')
    general_course_owner = data.get('general_course_owner')
    general_course = models.General(name=name, number=number, short_name=short_name, prerequisite=prerequisite, general_course_owner=general_course_owner)
    db.session.add(general_course)
    db.session.commit()
    
'''