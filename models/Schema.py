from models import ma, College, Department, Program, Course, General, Specific, Programspecificcourse

class CollegeSchema(ma.ModelSchema):
    class Meta:
        model = College

class DepartmentSchema(ma.ModelSchema):
    class Meta:
        model = Department

class ProgramSchema(ma.ModelSchema):
    class Meta:
        model = Program

class CourseSchema(ma.ModelSchema):
    class Meta:
        model = Course

class GeneralSchema(ma.ModelSchema):
    class Meta:
        model = General

class SpecificSchema(ma.ModelSchema):
    class Meta:
        model = Specific

class ProgramSpecificSchema(ma.ModelSchema):
    class Meta:
        model = Programspecificcourse

class CourseSchema(ma.ModelSchema):
    class Meta:
        model = Course
