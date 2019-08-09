from flask_wtf import FlaskForm
from wtforms import StringField,TextAreaField,SubmitField,SelectField
from wtforms.validators import Required

class PostForm(FlaskForm):
    title = StringField('Post title',validators=[Required()])
    description = TextAreaField('About Post')
    submit = SubmitField('Submit')
    
class UpdateProfile(FlaskForm):
    bio = TextAreaField('Tell us about you.',validators = [Required()])
    submit = SubmitField('Submit')
    
class CommentsForm(FlaskForm):
    comment = TextAreaField('Add your Comments', validators=[Required()])
    submit = SubmitField('Submit Comment')