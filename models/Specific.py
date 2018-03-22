from models.Course import Course
from models import db

class Specific(Course):
    """
        Model class for Specific Course entity
        Relationship: Many to Many Relationship with Programs.
    """

    __mapper_args__ = {'polymorphic_identity': 'specific'}

    id = db.Column(db.Integer, db.ForeignKey('course.id'), primary_key=True)
    units = db.Column(db.String(200))
    short_name = db.Column(db.String(100), nullable=False)
    name = db.Column(db.String(400), nullable=False)
    description = db.Column(db.String(5000))
    type = db.Column(db.String(1000))
    prerequisite = db.Column(db.String(2000))
    url = db.Column(db.String(1000))

    programid = db.Column(db.Integer, db.ForeignKey('program.id'))

    course = db.relationship('Program', secondary='programspecificcourse',
                             backref=db.backref('courses', lazy='dynamic'))
