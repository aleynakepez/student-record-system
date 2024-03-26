#these classes are used for creating forms with WTForms
from wtforms import Form,StringField,validators,IntegerField,DecimalField


class StudentForm(Form):
   student_name = StringField("Student name:", validators=[validators.InputRequired()])

class StudentInfoForm(Form):
   student_number = IntegerField("Student Number: ", validators=[validators.InputRequired()])
   student_grade = IntegerField("Grade: ", validators=[validators.InputRequired()])
   stuParentName = StringField("Parent Name: ", validators=[validators.InputRequired()])
   stuParentPhone =IntegerField("Student Phone: ", validators=[validators.InputRequired()])
   stuMail = StringField("Student Mail: ", validators=[validators.InputRequired()])
   stuGender = StringField("Student Gender: ", validators=[validators.InputRequired()])

class ExamsForm(Form):
   student_number = IntegerField("Student Number: ", validators=[validators.InputRequired()])
   math = IntegerField("Math: ", validators=[validators.InputRequired()])
   physics = IntegerField("Physics: ", validators=[validators.InputRequired()])
   biology =IntegerField("Biology: ", validators=[validators.InputRequired()])
   history =IntegerField("History: ", validators=[validators.InputRequired()])
   sports = IntegerField("Sports: ", validators=[validators.InputRequired()])

class AttendanceForm(Form):
   student_number = IntegerField("Student Number: ", validators=[validators.InputRequired()])
   math_absent = IntegerField("Math Absent: ", validators=[validators.InputRequired()])
   physics_absent = IntegerField("Physics Absent: ", validators=[validators.InputRequired()])
   biology_absent =IntegerField("Biology Absent: ", validators=[validators.InputRequired()])
   history_absent = IntegerField("History Absent: ", validators=[validators.InputRequired()])
   sports_absent = IntegerField("Sports Absent: ", validators=[validators.InputRequired()])