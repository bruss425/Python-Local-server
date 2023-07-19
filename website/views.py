from flask import Blueprint, render_template, request, flash, jsonify
from flask_login import login_required, current_user
from .models import Note, User
from . import db
import json

views = Blueprint('views', __name__)





@views.route('/', methods=['GET', 'POST'])
@login_required
def home():
    user = User.query.get(current_user.id)
    balance = user.balance1
    if request.method == 'POST': 
        note = request.form.get('note')#Gets the note from the HTML 
        

        if len(note) < 1:
            flash('Note is too short!', category='error') 
        else:
            new_note = Note(data=note, user_id=current_user.id)  #providing the schema for the note 
            db.session.add(new_note) #adding the note to the database 
            db.session.commit()
            flash('Note added!', category='success')

    return render_template("home.html", user=current_user,balance = balance)


@views.route('/delete-note', methods=['POST'])
def delete_note():  
    note = json.loads(request.data) # this function expects a JSON from the INDEX.js file 
    noteId = note['noteId']
    note = Note.query.get(noteId)
    if note:
        if note.user_id == current_user.id:
            db.session.delete(note)
            db.session.commit()

    return jsonify({})

@views.route('/account', methods=['GET'])
@login_required
def account_home():
    user = User.query.get(current_user.id)
    balance = user.balance1
    return render_template("account/base.html", user=current_user, balance = balance)

@views.route('/account/deposit', methods=['GET', 'POST'])
@login_required
def deposit():
    global balance
    user = User.query.get(current_user.id)
    balance = (int)(user.balance1)
    if request.method == 'POST': 
        try:
            new_balance = (int)(request.form.get('balance'))
        except:
             flash('Your input was not a number amount.', category='error')
        else: 
            user.balance1 = new_balance + balance
            db.session.commit()
            flash(('You have deposited $' + str(new_balance) + ".00 into your account."), category='success')
            balance = user.balance1
       
    return render_template("account/deposit.html", user=current_user, balance = balance)

@views.route('/account/withdraw', methods=['GET','POST'])
@login_required
def withdraw():
    global balance
    user = User.query.get(current_user.id)
    balance = (int)(user.balance1)
    if request.method == 'POST': 
        try:
            new_balance = (int)(request.form.get('balance'))
        except:
             flash('Your input was not a number amount.', category='error')
        else:
            if((balance - new_balance) < 0):
                flash('Your maximum amount to withdraw is $' + str(balance) + '.00', category='error')
            else: 
                user.balance1 = balance - new_balance
                db.session.commit()
                flash(('You have withdrawn $' + str(new_balance) + ".00 from your account."), category='success')
                balance = user.balance1
        
    return render_template("account/withdraw.html", user=current_user, balance = balance)


 

#api is next! 