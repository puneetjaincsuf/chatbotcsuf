from models import db
from models import ma
from models.Course import Course

class General(Course, db.Model):
    """
       Model class for General Course entity
       Relationship: One to many relationship with Department.
    """

    #[units, short_name, course_name, course_description, type, course_prerequisite, college_name];

    __mapper_args__ = {'polymorphic_identity': 'general'}

    id = db.Column(db.Integer, db.ForeignKey('course.id'), primary_key=True)

    units = db.Column(db.String(200))
    short_name = db.Column(db.String(50), nullable=False)
    name = db.Column(db.String(400), nullable=False)
    description = db.Column(db.String(5000))
    type = db.Column(db.String(1000))
    prerequisite = db.Column(db.String(1000))
    url = db.Column(db.String(1000))

    departmentid = db.Column(db.Integer, db.ForeignKey('college.id'))

    course = db.relationship('College', backref=db.backref('colleges', lazy='dynamic'))

