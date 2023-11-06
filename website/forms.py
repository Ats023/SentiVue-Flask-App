from flask_wtf import FlaskForm
from wtforms import StringField, FileField
from wtforms.validators import DataRequired

class ProjectForm(FlaskForm):
    title = StringField('Project Title', validators=[DataRequired()])
    desc = StringField('Project Title', validators=[DataRequired()])
    csv_data = FileField('Upload CSV', validators=[DataRequired()])