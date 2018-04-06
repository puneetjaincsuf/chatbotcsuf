import models
from scraper import College, Department, Program, GeneralCourses, SpecificCourses
import api.services
import settings

app = api.app
models.db.init_app(app)
models.db.app = app
models.ma.init_app(app)

app.config['SQLALCHEMY_DATABASE_URI'] = settings.SQLALCHEMY_DATABASE_URI
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True


def reset_database():
    """
    Recreate schema
    :return:
    """
    models.db.drop_all()
    models.db.create_all()


def create_colleges():
    """
    Create colleges and insert them into database

    :return:
    """
    try:
        print('Creating Colleges')
        colleges = College.get_colleges();
        for url, clg in colleges.items():
            college = models.College(name=clg[0], description=clg[1], short_name="", url = url)
            models.db.session.add(college)
        models.db.session.commit()
    except Exception as e:
        print("Error Occured"+ e)


def create_departments():
    """
    Create departments and insert them into database
    :return:
    """
    try:
        print('Creating Departments')
        departments = Department.get_departments()
        for url, dept in departments.items():
            college = models.db.session.query(models.College).filter(models.College.name == dept[2][0]).one()
            department = models.Department(name=dept[0], short_name="", description=dept[1], department_owner=college, url = url)
            models.db.session.add(department)
        models.db.session.commit()
    except Exception as e:
        print("Error Occured" + e)


def create_programs():
    """
    Create programs and insert them into database

    :return:
    """
    try:
        print('Creating Programs')
        programs = Program.get_programs()
        for url, prog in programs.items():
            department = models.db.session.query(models.Department).filter(models.Department.name == prog[1]).one()
            program = models.Program(name=prog[0], short_name="", type=prog[2], program_owner=department, url = url)
            models.db.session.add(program)
        models.db.session.commit()
    except Exception as e:
        print("Error Occured" + e)


def create_general_courses():
    """
    Create general courses and insert them into database

    :return:
    """
    try:
        print('Creating General Courses')
        general_courses = GeneralCourses.get_general_courses()
        for url, gc in general_courses.items():
            college = models.db.session.query(models.College).filter(models.College.name == gc[6]).one()
            general_course = models.General(units=gc[0], short_name=gc[1], name=gc[2], description = gc[3],
                                            type = gc[4], prerequisite = gc[5], url = url,
                                            general_course_owner=college)
            models.db.session.add(general_course)
        models.db.session.commit()
    except Exception as e:
        print("Error Occured" + e)


def create_specific_courses():
    """
    Create specific courses and insert them into database

    :return:
    """
    try:
        print('Creating Specific Courses')
        specific_courses = SpecificCourses.get_specific_courses()
        for url, sc in specific_courses.items():
            program = models.db.session.query(models.Program).filter(models.Program.name == sc[6]).one()
            specific_course = models.Specific(units=sc[0], short_name=sc[1], name=sc[2], description = sc[3],
                                            type = sc[4], prerequisite = sc[5], url = url,
                                            specific_course_owner=program)
            models.db.session.add(specific_course)
        models.db.session.commit()
    except Exception as e:
        print("Error Occured" + e)


reset_database()
create_colleges()
create_departments()
create_programs()
create_general_courses()
create_specific_courses()