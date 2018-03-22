from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow

db = SQLAlchemy()
ma = Marshmallow()

__all__ = ["Department", "College", "Course", "Program", "General", "Specific", "Programspecificcourse"]#, "CollegeSchema", "ProgramSchema", "DepartmentSchema"]

from models.College import College
from models.Course import Course
from models.Department import Department
from models.Program import Program
from models.General import General
from models.Specific import Specific
from models.Programspecificcourse import Programspecificcourse
from models.Schema import CollegeSchema, ProgramSchema, DepartmentSchema, GeneralSchema, SpecificSchema, CourseSchema


def reset_database():
    db.drop_all()
    db.create_all()

def create_database():
    db.create_all()

