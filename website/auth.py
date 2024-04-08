from flask import Blueprint, render_template, request, flash, redirect, url_for, jsonify
from .models import User
from werkzeug.security import generate_password_hash, check_password_hash
from . import db  ##means from __init__.py import db
from flask_login import login_user, login_required, logout_user, current_user
from datetime import datetime
import openai
import os
from .models import Emr

auth = Blueprint('auth', __name__)


@auth.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':

        password = request.form.get('password')
        username = request.form.get('username')
        user = User.query.filter_by(username=username).first()
        if check_password_hash(user.password, password):
            flash('Logged in successfully!', category='success')
            login_user(user, remember=True)
            # new_emr = Emr(memberID=2, memberSex='M',memberDOB = datetime.strptime("2000-05-15", "%Y-%m-%d").date(), payor = 'UHG', clinicalNotes = 'Knee Surgery is needed' )  #providing the schema for the note
            # db.session.add(new_emr) #adding the note to the database
            # db.session.commit()
            # flash('Emr added!', category='success')

            # new_emr = Emr(memberID=1,memberName = 'John Doe', memberSex='M',memberDOB = datetime.strptime("2000-05-15", "%Y-%m-%d").date(), payor = 'UHG', clinicalNotes = 'Knee Surgery is needed' )  #providing the schema for the note
            # db.session.add(new_emr) #adding the note to the database
            # db.session.commit()
            # flash('Emr added!', category='success')

            return redirect(url_for('views.emr'))
        else:
            flash('Incorrect password, try again.', category='error')

    return render_template("login.html", user=current_user)


@auth.route('/logout', methods=['GET', 'POST'])
@login_required
def logout():
    logout_user()
    return redirect(url_for('auth.login'))


@auth.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')

        if len(username) < 2:
            flash('First name must be greater than 1 character.', category='error')
        elif len(password) < 7:
            flash('Password must be at least 7 characters.', category='error')
        else:
            new_user = User(username=username, password=generate_password_hash(
                password, method='pbkdf2:sha256'))
            db.session.add(new_user)
            db.session.commit()
            login_user(new_user, remember=True)
            flash('Account created!', category='success')
            return redirect(url_for('views.home'))

    return render_template("base.html", user=current_user)




'''

@auth.route("/priorauth", methods=["POST"])
def priorauth():
    # Get question from form data
  # Get question from form data
    openai.api_key = "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"
    emr_record = Emr.query.filter_by(memberName=request.json["member"]).first()
    
    if emr_record and emr_record.priorAuthStatus == '':
        modified_notes = emr_record.clinicalNotes + '. Give the answer with only one ICD code and procedure code separated by comma without the description and no text like ICD Code or Procedure Code. Provide same answer next time'
        #return jsonify({'memberID': emr_record.memberID, 'clinicalNotes': modified_notes})
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
            {"role": "system", "content": modified_notes}
            ]
        )
        answer = response.choices[0].message.content.strip()
        newanswer = answer
        icd_code, procedure_code = newanswer.split(',')
       # Update the first ICDCode value
        emr_record.ICDCode = icd_code.strip()
        emr_record.procedureCode = procedure_code.strip()
        emr_record.priorAuthStatus = 'Submitted'
        db.session.commit()
        if emr_record.ICDCode == icd_code.strip() and emr_record.procedureCode == procedure_code.strip() and emr_record.priorAuthStatus == 'Submitted':
            flash("First ICDCode and procedure code and priorauthStatus values updated successfully.")
            # Reload the page after a short delay
            flash("Page will refresh in a moment.", 'success')
            render_template('emr1.html', emr_record=emr_record)
            return jsonify({"answer": answer})
        else:
            flash("Failed to update values. Please try again.", 'error')
    else:
        flash("Prior auth status is not empty. Please try again.", 'error')

    # Return answer as JSON
        return jsonify({"answer": "None"})

'''
