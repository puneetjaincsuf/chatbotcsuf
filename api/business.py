from models import db
import models

"""
This file is currently not in use.
"""


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