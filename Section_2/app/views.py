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
    expenditure = None
    form = AddIncomeExpenditureForm()
    if form.validate_on_submit():
        if request.method == 'POST':
            name = request.form['name']
            amount = request.form['amount']

            expenditure = models.Expenditure.query.filter_by(name=name).first()
            
            try:
                if expenditure:
                    flash('Expenditure with that name already exists!', 'danger')
                else:
                    flash('Successfully added expenditure!', 'success')
                    expenditure = models.Expenditure(name=name, amount=amount)
                    db.session.add(expenditure)
                    db.session.commit()
                
                return redirect(url_for('addExpenditure'))

            except:
                return "There was an error adding the expenditure!"
        
    else:
        expenditure = models.Expenditure.query.order_by(models.Expenditure.date_created)

    return render_template('create.html',
                            title='Expenditure',
                            form=form,
                            expenditure=expenditure)