from flask import render_template, flash, request, session, redirect, url_for #Added request session redirect, url_for
from app import app, db, models # Added db and models subsequently.
from .forms import CalculatorForm, AddIncomeExpenditureForm

@app.route('/', methods=['GET', 'POST'])
def index():
    user = {'name': 'Sam Wilson'}
    return render_template('index.html',
                           title='Simple template example',
                           user=user)

@app.route('/fruit')
def displayFruit():
    fruits = ["Apple", "Banana", "Orange", "Kiwi"]
    return render_template("fruit_with_inheritance.html",fruits=fruits)

@app.route('/calculator', methods=['GET', 'POST'])
def calculator():
    form = CalculatorForm()
    if form.validate_on_submit():
        flash('Succesfully received form data. %s + %s  = %s'%(form.number1.data, form.number2.data, form.number1.data+form.number2.data))
    return render_template('calculator.html',
                           title='Calculator',
                           form=form)


@app.route('/income', methods=['GET', 'POST'])
def addIncome():
    form = AddIncomeExpenditureForm()
    if form.validate_on_submit():
        flash('Yay, added income')
    return render_template('create.html',
                            title='Income',
                            form=form)

@app.route('/expenditure', methods=['GET', 'POST'])
def addExpenditure():
    form = AddIncomeExpenditureForm()
    if form.validate_on_submit():
        if request.method == 'POST':
            name = request.form['name']
            amount = request.form['amount']

            income = models.Income.query.filter_by(name='test23').first()
            flash(income)
            flash(f'{name}, {amount}')

            if income:
                flash('Already there')
            else:
                flash('New data')
                test = models.Income(name='test12344', amount='23')
                db.session.add(test)
                db.session.commit()

        flash('Yay, added expenditure')

    return render_template('create.html',
                            title='Expenditure',
                            form=form)