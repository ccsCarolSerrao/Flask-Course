from flask_wtf import FlaskForm as Form
from wtforms.fields import StringField, PasswordField, BooleanField, SubmitField
from flask.ext.wtf.html5 import URLField
from wtforms.validators import DataRequired, url, Length, Email, EqualTo, Regexp, ValidationError
from .. models import User

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
    nm_url = URLField('The URL for your bookmark:', validators=[DataRequired(message='Input an URL'), url()])
    nm_description = StringField('Add an optional description:')
    tags = StringField('Tags:', validators=[Regexp('^[A-Za-z0-9, ]*$', message='Tags consit of letters and numbers.')])

    def validate(self):
        if not (self.nm_url.data.startswith('https://') or self.nm_url.data.startswith('http://')):
            self.nm_url.data = "http://" + self.nm_url.data

        if not Form.validate(self):
            return False

        if not self.nm_description.data:
            self.nm_description.data = self.nm_url.data
        
        #filter our empty and duplicate tag names
        stripped = [t.strip() for t in self.tags.data.split(',')] #retira os espaços
        not_empty = [tag for tag in stripped if tag] #retira os vazios
        tagset = set(not_empty) #retira os duplicados
        self.tags.data = ','.join(tagset)

        return True
        