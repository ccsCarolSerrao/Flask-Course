from flask_wtf import FlaskForm as Form
from wtforms.fields import StringField, PasswordField, BooleanField, SubmitField
from flask.ext.wtf.html5 import URLField
from wtforms.validators import DataRequired, url, Length, Email, EqualTo, Regexp, ValidationError
from . models import User

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

class SingupForm(Form): 
    '''Create an Form Object to Validate LoginForm
        Arguments:
            Form - Form Objetct - SingupForm
        Validator:
    '''   
    firstname = StringField('First Name:', 
                            validators=[
                                DataRequired(), Length(1, 120),
                                Regexp('^[A-Za-z ]{1,}$',
                                        message='Username consit of letters.')
                            ])
    lastname = StringField('Last Name:', 
                            validators=[
                                DataRequired(), Length(1, 120),
                                Regexp('[A-Za-z ]{1,}$',
                                        message='Username consit of letters.')
                            ])
    email = StringField('E-mail:', validators= [DataRequired(), Length(1, 120), Email()])                            
    username = StringField('Username:', 
                            validators=[
                                DataRequired(), Length(3, 80),
                                Regexp('^[A-Za-z0-9_]{3,}$',
                                        message='Username consit of numbers, letters and underscores.')
                            ])
    password = PasswordField('Password:', 
                            validators=[
                                DataRequired(), Length(6,),
                                EqualTo('password2',
                                        message='Password must match.')
                            ])
    password2 = PasswordField('Confirm Password:', validators=[DataRequired(), Length(6,)])

    def validate_email(self, email_field):
        if User.get_by_email(email_field.data):
            raise ValidationError('There already is an user with this email adress.')
    
    def validate_username(self, username_field):
        if User.query.filter_by(nm_userName=username_field.data).first():
            raise ValidationError('This username is already taken.')            