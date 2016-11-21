from flask_wtf import FlaskForm as Form
from wtforms.fields import StringField, PasswordField, BooleanField, SubmitField
from wtforms.validators import DataRequired, Length, Email, EqualTo, Regexp, ValidationError
from .. models import User

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
    nm_userName = StringField('Your UserName:', validators=[DataRequired()])
    nm_password = PasswordField('Password:', validators=[DataRequired()]) 
    remember_me = BooleanField('Keep me logged in')
    submit = SubmitField('Log In')  

class SingupForm(Form): 
    '''Create an Form Object to Validate LoginForm
        Arguments:
            Form - Form Objetct - SingupForm
        Validator:
    '''   
    nm_firstName = StringField('First Name:', 
                            validators=[
                                DataRequired(), Length(1, 120),
                                Regexp('^[A-Za-z ]{1,}$',
                                        message='Username consit of letters.')
                            ])
    nm_lastName = StringField('Last Name:', 
                            validators=[
                                DataRequired(), Length(1, 120),
                                Regexp('[A-Za-z ]{1,}$',
                                        message='Username consit of letters.')
                            ])
    nm_email = StringField('E-mail:', validators= [DataRequired(), Length(1, 120), Email()])                            
    nm_userName = StringField('Username:', 
                            validators=[
                                DataRequired(), Length(3, 80),
                                Regexp('^[A-Za-z0-9_]{3,}$',
                                        message='Username consit of numbers, letters and underscores.')
                            ])
    nm_password = PasswordField('Password:', 
                            validators=[
                                DataRequired(), Length(6,),
                                EqualTo('nm_password2',
                                        message='Password must match.')
                            ])
    nm_password2 = PasswordField('Confirm Password:', validators=[DataRequired(), Length(6,)])

    def validate_email(self, nm_email_field):
        if User.get_by_email(nm_email_field.data):
            raise ValidationError('There already is an user with this email adress.')
    
    def validate_username(self, nm_userName_field):
        if User.query.filter_by(nm_userName=nm_userName_field.data).first():
            raise ValidationError('This username is already taken.')    