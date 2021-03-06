"""
form_register_immediate.py
This file contains login form stuff
"""


# mewlo imports
from mewlo.mpacks.core.form.mform import MewloForm, BigStringField

# library imports
from wtforms import Form, BooleanField, StringField, PasswordField, validators

# python imports





class MewloForm_Register_Immediate(MewloForm):

    username = StringField('Username', [validators.Length(min=3, max=32)])
    password = PasswordField('Password', [validators.Length(min=3, max=64)])
    email = BigStringField('Email Address', [validators.Length(min=6, max=64)])
    #accept_rules = BooleanField('I accept the site rules', [validators.InputRequired()])

    #
    viewfilename = 'register_immediate.jn2'

    def __init__(self, *args, **kwargs):
        # parent constructor
        super(MewloForm_Register_Immediate, self).__init__(*args, **kwargs)

