from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, SubmitField
from wtforms.validators import DataRequired

class CreateProjectForm(FlaskForm):
	title_uk = StringField("Заголовок (укр)", validators=[DataRequired()])
	title_de = StringField("Titel (de)", validators=[DataRequired()])
	desc_uk = TextAreaField("Опис (укр)", validators=[DataRequired()])
	desc_de = TextAreaField("Beschreibung (de)", validators=[DataRequired()])
	submit = SubmitField("Подати")
