from models import db


class College(db.Model):

    """
    Model class for College entity
    Relationship: One to many relationship with Department.
    """

    id = db.Column(db.Integer, nullable=False, primary_key=True)
    name = db.Column(db.String(400))
    description = db.Column(db.String(5000))
    short_name = db.Column(db.String(50))
    url = db.Column(db.String(1000))
    department = db.relationship('Department', backref='department_owner', lazy='dynamic')

    general_course = db.relationship('General', backref='general_course_owner', lazy='dynamic')
