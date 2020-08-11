from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, TextAreaField
from wtforms.validators import DataRequired
from flask_wtf.file import FileField, FileAllowed

class PostForm(FlaskForm):
    files =  FileField('Upload Files', validators=[FileAllowed(['txt', 'pdf'])])
    submit = SubmitField('Post')

class EditForm(FlaskForm):
    name = StringField(validators=[DataRequired()])
    submit = SubmitField('Post')

class SearchForm(FlaskForm):
    filename = StringField(validators=[DataRequired()])
    submit = SubmitField('search')