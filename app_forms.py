from wtforms import Form, SelectField, SubmitField, validators, RadioField

class MenuForm(Form,choices):
    Monday = SelectField("Monday", choices=choices)
    
