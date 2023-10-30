from flask import render_template, flash, request, session, redirect, url_for #Added request session redirect, url_for
from app import app, db, models # Added db and models subsequently.
from .forms import CalculatorForm, AddIncomeExpenditureForm, AddSavingsGoalForm
from sqlalchemy import or_ # Added to combine results on home page

import json

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

    # Check if savings exists.
    savingsGoal = models.Savings.query.limit(1).all()

    # Sort the combined results by creation time of user using a lambda function.
    income_and_expenditure.sort(key=lambda x: x.date_created)

    return render_template('index.html',
                           title='Home Page',
                           income_and_expenditure=income_and_expenditure,
                           total_income=total_income,
                           total_expenditure=total_expenditure,
                           total_difference=total_difference,
                           savingsGoal=savingsGoal)

@app.route('/income', methods=['GET', 'POST'])
def addIncome():
    form = AddIncomeExpenditureForm()
    
    if form.validate_on_submit():
        if request.method == 'POST':
            name = request.form['name']
            amount = request.form['amount']

            income = models.Income.query.filter_by(name=name).first()
            
            try:
                if income:
                    flash('Income with that name already exists!', 'info')
                else:
                    income = models.Income(name=name, amount=amount)
                    db.session.add(income)
                    db.session.commit()
                    flash('Successfully added income!', 'success')
                
                return redirect(url_for('addIncome'))

            except:
                return "There was an error adding the income!"
        
    income = models.Income.query.order_by(models.Income.date_created).all()

    return render_template('create.html',
                            title='Add Income',
                            form=form,
                            income=income)


@app.route('/expenditure', methods=['GET', 'POST'])
def addExpenditure():
    form = AddIncomeExpenditureForm()
    
    if form.validate_on_submit():
        if request.method == 'POST':
            name = request.form['name']
            amount = request.form['amount']

            expenditure = models.Expenditure.query.filter_by(name=name).first()
            
            try:
                if expenditure:
                    flash('Expenditure with that name already exists!', 'info')
                else:
                    flash('Successfully added expenditure!', 'success')
                    expenditure = models.Expenditure(name=name, amount=amount)
                    db.session.add(expenditure)
                    db.session.commit()
                
                return redirect(url_for('addExpenditure'))

            except:
                return "There was an error adding the expenditure!"
        
    expenditure = models.Expenditure.query.order_by(models.Expenditure.date_created).all()

    return render_template('create.html',
                            title='Add Expenditure',
                            form=form,
                            expenditure=expenditure)


@app.route('/savings', methods=['GET', 'POST'])
def add_goal():
    form = AddSavingsGoalForm()
    final_data_json = None
    final_amount = None

    existing_savings_goal = models.Savings.query.first()
    
    if request.method == 'POST':
        if existing_savings_goal:
            flash('A savings goal already exists. Only one savings goal is allowed at a time.', 'danger')
            return redirect(url_for('add_goal'))

        name = form.name.data
        goal_amount = form.amount.data

        savings_goal = models.Savings(name=name, goal_amount=goal_amount)
        db.session.add(savings_goal)
        db.session.commit()

        return redirect(url_for('add_goal'))

    if existing_savings_goal:
        income_entries = models.Income.query.all()
        expenditure_entries = models.Expenditure.query.all()

        income_entries_with_type = [(entry, "Income") for entry in income_entries]
        expenditure_entries_with_type = [(entry, "Expenditure") for entry in expenditure_entries]

        new_income_and_expenditure = income_entries_with_type + expenditure_entries_with_type

        new_income_and_expenditure.sort(key=lambda x: x[0].date_created)

        # Now you can iterate through income_and_expenditure and access each entry and its type
        data_x_axis = []
        current_balance = 0

        # Instantiate 0
        data_x_axis.append(current_balance)

        for entry, entry_type in new_income_and_expenditure:
            if entry_type == "Income":
                current_balance += entry.amount
            else:  # It's an expenditure
                current_balance -= entry.amount
            data_x_axis.append(current_balance)


        final_data_json = json.dumps(data_x_axis)
        final_amount = data_x_axis[-1]


    return render_template('savings.html',
                           title='Add Savings Goal' if not existing_savings_goal else 'Savings Goal',
                           form=form,
                           existing_savings_goal=existing_savings_goal,
                           final_data=final_data_json,
                           final_amount=final_amount)


@app.route('/savings/update', methods=['GET', 'POST'])
def update_goal():
    form = AddSavingsGoalForm()
    savings = models.Savings.query.first()

    if not savings:
        flash('Savings Goal does not exist!', 'danger')
        return redirect(url_for('add_goal'))

    if form.validate_on_submit():
        name = request.form['name']
        amount = request.form['amount']

        try:
            savings.name = name
            savings.goal_amount = amount
            db.session.commit()
            flash('Successfully updated savings goal!', 'success')
            return redirect(url_for('add_goal'))
        except:
            return "There was an error updating the entry!"

    form.name.data = savings.name
    form.amount.data = savings.goal_amount

    return render_template('update.html',
                           title='Update Savings Goal',
                           form=form)


@app.route('/savings/delete', methods=['GET', 'POST'])
def delete_goal():
    savings = models.Savings.query.first()

    try:
        if savings:
            db.session.delete(savings)
            db.session.commit()
            flash('Successfully deleted goal!', 'success')

            return redirect(url_for('add_goal'))
        else:
            flash('Savings goal does not exist!', 'danger')
            return redirect(url_for('add_goal'))

    except:
        flash('There was an error deleting the entry!', 'danger')

@app.route('/<entry_type>/update/<int:id>', methods=['GET', 'POST'])
def update_entry(entry_type, id):
    form = AddIncomeExpenditureForm()

    if entry_type == 'income':
        entry = models.Income.query.get_or_404(id)
        existing_entry = models.Income.query.filter_by(name=form.name.data).first()
    elif entry_type == 'expenditure':
        entry = models.Expenditure.query.get_or_404(id)
        existing_entry = models.Expenditure.query.filter_by(name=form.name.data).first()

    if form.validate_on_submit():
        name = request.form['name']
        amount = request.form['amount']
        
        if existing_entry:
            flash('An entry with the same name already exists.', 'warning')
            return redirect(url_for('update_entry', entry_type=entry_type, id=id))

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
                            form=form)

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
