from flask_wtf import FlaskForm
from wtforms import DecimalField, StringField
from wtforms.validators import DataRequired, Length, NumberRange
    
class AddIncomeExpenditureForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired(), Length(min=1, max=50)])
    amount = DecimalField('Amount', validators=[DataRequired(), NumberRange(min=1)])

class AddSavingsGoalForm(FlaskForm):
    name = StringField('Name', validators=[Length(min=1, max=50)])
    amount = DecimalField('Amount', validators=[DataRequired(), NumberRange(min=1)])