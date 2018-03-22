from models import db
from models import ma

class Program(db.Model):
    """
       Model class for Program entity.
       Relationship: Many to Many relationship with Specific Courses.
    """
    id = db.Column(db.Integer, nullable=False, primary_key=True)
    name = db.Column(db.String(400))
    type = db.Column(db.String(50))
    short_name = db.Column(db.String(50))
    url = db.Column(db.String(1000))
    department = db.Column(db.Integer, db.ForeignKey('department.id'))
    specific_course = db.relationship('Specific', backref='specific_course_owner', lazy='dynamic')
