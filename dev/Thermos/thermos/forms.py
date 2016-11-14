from flask_wtf import FlaskForm as Form
from wtforms.fields import StringField, PasswordField, BooleanField, SubmitField
from flask.ext.wtf.html5 import URLField
from wtforms.validators import DataRequired, url

class BookmarkForm(Form):
    '''Create an Form Object to Validate
        Arguments:
            Form - Form Objetct - BookmarkForm
        Validator:
            url:
                has value - DataRequired()
                valid url input - url()
            description:
    '''
    url = URLField('The URL for your bookmark:', validators=[DataRequired(message='Input an URL'), url()])
    description = StringField('Add an optional description:')

    def validate(self):
        if not (self.url.data.startswith('https://') or self.url.data.startswith('http://')):
            self.url.data = "http://" + self.url.data

        if not Form.validate(self):
            return False

        if not self.description.data:
            self.description.data = self.url.data

        return True

class LoginForm(Form):
    '''Create an Form Object to Validate LoginForm
        Arguments:
            Form - Form Objetct - LoginForm
        Validator:
            url:
                has value - DataRequired()
                valid url input - url()
            description:
    '''
    username = StringField('Your UserName:', validators=[DataRequired()])
    password = PasswordField('Password:', validators=[DataRequired()]) 
    remember_me = BooleanField('Keep me logged in')
    submit = SubmitField('Log In')  