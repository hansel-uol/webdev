from flask_wtf import FlaskForm
from wtforms import IntegerField
from wtforms import TextAreaField
from wtforms.validators import DataRequired

class CalculatorForm(FlaskForm):
    number1 = IntegerField('number1', validators=[DataRequired()])
    number2 = IntegerField('number2', validators=[DataRequired()])
    date = TextAreaField()
    