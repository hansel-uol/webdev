from flask import render_template, flash, request, session, redirect, url_for #Added request session redirect, url_for
from app import app, db, models # Added db and models subsequently.
from .forms import CalculatorForm, AddIncomeExpenditureForm
from sqlalchemy import or_ # Added to combine results on home page

@app.route('/', methods=['GET', 'POST'])
def index():
    # Query each table.
    income_entries = models.Income.query.all()
    expenditure_entries = models.Expenditure.query.all()
    
    # Calculate values and pass them to the template.
    total_income = sum(entry.amount for entry in income_entries)
    total_expenditure = sum(entry.amount for entry in expenditure_entries)
    total_difference = total_income - total_expenditure

    # Combine the results from both tables.
    income_and_expenditure = income_entries + expenditure_entries

    # Sort the combined results by creation time of user using a lambda function.
    income_and_expenditure.sort(key=lambda x: x.date_created, reverse=False)

    return render_template('index.html',
                           title='Home Page',
                           income_and_expenditure=income_and_expenditure,
                           total_income=total_income,
                           total_expenditure=total_expenditure,
                           total_difference=total_difference)


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
    income = None
    form = AddIncomeExpenditureForm()
    if form.validate_on_submit():
        if request.method == 'POST':
            name = request.form['name']
            amount = request.form['amount']

            income = models.Income.query.filter_by(name=name).first()
            
            try:
                if income:
                    flash('Income with that name already exists!', 'danger')
                else:
                    flash('Successfully added income!', 'success')
                    income = models.Income(name=name, amount=amount)
                    db.session.add(income)
                    db.session.commit()
                
                return redirect(url_for('addIncome'))

            except:
                return "There was an error adding the income!"
        
    else:
        income = models.Income.query.order_by(models.Income.date_created)

    return render_template('create.html',
                            title='Income',
                            form=form,
                            income=income)

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


@app.route('/<entry_type>/update/<int:id>', methods=['GET', 'POST'])
def update_entry(entry_type, id):
    form = AddIncomeExpenditureForm()
    if entry_type == 'income':
        entry = models.Income.query.get_or_404(id)
    elif entry_type == 'expenditure':
        entry = models.Expenditure.query.get_or_404(id)

    if form.validate_on_submit():
        name = request.form['name']
        amount = request.form['amount']

        try:
            entry.name = name
            entry.amount = amount
            db.session.commit()
            flash('Successfully updated entry!', 'success')
            return redirect(url_for('index'))
        except:
            return "There was an error updating the entry!"

    form.name.data = entry.name
    form.amount.data = entry.amount

    return render_template('update.html',
                            title='Update ' + entry_type.capitalize(),
                            form=form,
                            entry=entry)


@app.route('/<entry_type>/delete/<int:id>')
def delete_entry(entry_type, id):
    if entry_type == 'income':
        entry = models.Income.query.get_or_404(id)
    elif entry_type == 'expenditure':
        entry = models.Expenditure.query.get_or_404(id)

    try:
        db.session.delete(entry)
        db.session.commit()
        flash('Successfully deleted entry!', 'success')

        # Depending on the URL that called the delete.
        # [Either home or /addIncome or /addExpenditure] redirect the URL accordingly.
        referrer = request.referrer
        if referrer:
            return redirect(referrer)
        else:
            return redirect(url_for('add' + entry_type.capitalize()))

    except:
        return "There was an error deleting the entry!"
