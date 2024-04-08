from flask import Blueprint, render_template, request, flash, jsonify
from flask_login import login_required, current_user
from .models import Emr
from . import db
import json

views =  Blueprint('views',__name__)

@views.route('/')

def home():
   return render_template("login.html")

@views.route('/emr') 
def emr():
   emr_data = Emr.query.all()
   memberName = db.session.query(Emr.memberName).distinct().all()
   member_list = [id[0] for id in memberName]
   flash(member_list)
 
   return render_template('emr1.html', emr_data=emr_data, member_list=member_list)

@views.route('/api', methods=["POST"])
def api():
    if request.method == "POST":
        selected_member = request.json.get("member")
        emr_details = Emr.query.filter_by(memberName=selected_member).all()
        formatted_details = [{
            "memberID": detail.memberID,
            "memberName": detail.memberName,
            "memberSex": detail.memberSex,
            "memberDOB": detail.memberDOB,
            "payor": detail.payor,
            "clinicalNotes": detail.clinicalNotes,
            "ICDCode": detail.ICDCode,
            "procedureCode": detail.procedureCode,
            "priorAuthStatus": detail.priorAuthStatus

        } for detail in emr_details]
        return jsonify({"emr_details": formatted_details})


@views.route('/priorauth', methods=['POST'])
def priorauth():
    try:
        selected_member = request.json.get('member')
        emr_record = Emr.query.filter_by(memberName=selected_member).first()

        if emr_record:
            # Update Prior Auth status to 'Submitted'
            emr_record.priorAuthStatus = 'Submitted'
            db.session.commit()

            flash(f"Prior Auth submitted successfully for {emr_record.memberName}", 'success')
            return jsonify({
                'success': True,
                'message': f"Prior Auth submitted successfully for {emr_record.memberName}",
                'emr_record': {
                    'memberName': emr_record.memberName,
                    'priorAuthStatus': emr_record.priorAuthStatus
                }
            }), 200
        else:
            flash("EMR record not found", 'error')
            return jsonify({'error': 'EMR record not found'}), 404

    except Exception as e:
        flash(f"Error submitting Prior Auth: {str(e)}", 'error')
        return jsonify({'error': f"Error submitting Prior Auth: {str(e)}"}), 500





