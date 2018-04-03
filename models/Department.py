from models import db
from models import ma


class Department(db.Model):

    """
       Model class for Department entity.
       Relationships: One to Many relationship with Programs and General Courses
    """

    id = db.Column(db.Integer, nullable=False, primary_key=True)
    name = db.Column(db.String(400))
    short_name = db.Column(db.String(50))
    description = db.Column(db.String(5000))
    url = db.Column(db.String(1000))
    college = db.Column(db.Integer, db.ForeignKey('college.id'))

    programs = db.relationship('Program', backref='program_owner', lazy='dynamic')
