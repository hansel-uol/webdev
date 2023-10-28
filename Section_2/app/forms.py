from flask_wtf import FlaskForm
from wtforms import IntegerField, DecimalField, TextAreaField, StringField, SubmitField
from wtforms.validators import DataRequired

class CalculatorForm(FlaskForm):
    number1 = IntegerField('number1', validators=[DataRequired()])
    number2 = IntegerField('number2', validators=[DataRequired()])
    date = TextAreaField()
    
class AddIncomeExpenditureForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired()])
    amount = DecimalField('Amount', validators=[DataRequired()])

    # submit = SubmitField('Submit')