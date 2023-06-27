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

@views.route('/account', methods=['GET', 'POST'])
@login_required
def account():
    global balance
    user = User.query.get(current_user.id)
    balance = user.balance1
    if request.method == 'POST': 
        new_balance = (request.form.get('balance'))
        user.balance1 = new_balance
        db.session.commit()
        flash('Your account balance has been changed.', category='success')
        balance = user.balance1
    return render_template("account.html", user=current_user, balance = balance)