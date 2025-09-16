from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, SubmitField
from wtforms.validators import DataRequired

# 12 запитань анкети — як приклад; доповнимо пізніше
class MemberSurveyForm(FlaskForm):
    q1 = StringField("Питання 1", validators=[DataRequired()])
    q2 = StringField("Питання 2")
    q3 = StringField("Питання 3")
    q4 = StringField("Питання 4")
    q5 = StringField("Питання 5")
    q6 = StringField("Питання 6")
    q7 = StringField("Питання 7")
    q8 = StringField("Питання 8")
    q9 = StringField("Питання 9")
    q10 = StringField("Питання 10")
    q11 = StringField("Питання 11")
    q12 = TextAreaField("Питання 12 (розширена відповідь)")
    submit = SubmitField("Зберегти")