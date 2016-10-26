from wtforms import Form, BooleanField,  StringField, PasswordField, validators


class WelcomeScreenForm(Form):
    site_to_parse = StringField('Site to parse', [validators.Length(min=4, max=25)])
    email = StringField('Email Address', [validators.Length(min=6, max=35)])
    password = PasswordField('New Password', [
        validators.DataRequired(),
        validators.EqualTo('confirm', message='Passwords must match')
    ])
    confirm = PasswordField('Repeat Password')

class CreateObjectForm(Form):
    object_name = StringField('object_name', [validators.Length(min=1, max=32)])
    object_attr = StringField('object_attr', [validators.Length(min=1, max=32)])

