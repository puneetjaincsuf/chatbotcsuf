from models import db
from models import ma

class Programspecificcourse(db.Model):
    """
    This model is a association between programs and specific courses.
    Program and Specific Course have many to many relationship.

    The ProgramSpecificCourse association table will have two columns:

        Specific Course Id
        Program Id

    """
    id = db.Column(db.Integer, nullable=False, primary_key=True)
    course = db.Column('course_id', db.Integer, db.ForeignKey('specific.id'))
    program = db.Column('program_id', db.Integer, db.ForeignKey('program.id'))
