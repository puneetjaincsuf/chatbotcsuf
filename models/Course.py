from models import db
from models import ma

class Course(db.Model):
    """
       Model class for Course entity. Course is super class for General and Specific Courses.
       polymorphic on coursetype
    """

    id = db.Column(db.Integer, primary_key=True)
    coursetype = db.Column(db.String(1000))

    __mapper_args__ = {'polymorphic_on': coursetype}
