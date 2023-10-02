from flask import Flask, jsonify, request, render_template, redirect
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from flask_qrcode import QRcode
from flask_cors import CORS, cross_origin
from datetime import datetime

# SETTINGS
app_title = 'LPU-Laguna Feedback System'
base_url = 'http://127.0.0.1:5000'

# Init Flask App
app = Flask(__name__)
cors = CORS(app)
QRcode(app)

# Init Database Connection
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///feedback.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# Init Mashmallow (serializer)
ma = Marshmallow(app)

# DATABASE SCHEMA DEFINITION
# Refer to `../docs/02-erd.md` for details
class Department(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    department = db.Column(db.String(200), nullable=False, default='')

    def __init__(self, department):
         self.department = department

class Feedback(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    department_id = db.Column(db.Integer, db.ForeignKey('department.id'), nullable=False)
    rating = db.Column(db.Integer, nullable=False)
    message = db.Column(db.String(10000), default=False) # I don't it's gonna go beyond this.
    date_created = db.Column(db.String(200), default=datetime.utcnow)

    def __init__(self, department_id, message, rating):
         self.department_id = department_id
         self.message = message
         self.rating = rating

# Marshmallow Schemas
class DepartmentSchema(ma.Schema):
    class Meta:
        fields = ('id', 'department')

class FeedbackSchema(ma.Schema):
    class Meta:
        fields = ('id', 'department_id', 'department', 'rating', 'message', 'date_created')

# Init Marshmallow Schemas
departments_schema = DepartmentSchema(many=True)
feedbacks_schema = FeedbackSchema()

# Run Database Migration
with app.app_context():
    db.create_all()
    all_departments = Department.query.all()
    if len(all_departments) == 0:
        print('Creating seed departments...')
        departments = ['HRDMO', 'MARKETING', 'ACCOUNTING', 'HIGH SCHOOL PRINCIPAL / PEAC', 'EXECUTIVE OFFICE', 'CLINIC', 'TREASURY', 'REGISTRAR', 'SECURITY', 'RESEARCH', 'MIS', 'OSAS', 'JR HIGH SCHOOL', 'SR HIGH SCHOOL', 'PPFO (Facilities)', 'PURCHASING / MMO', 'CAS', 'CBA', 'GUIDANCE', 'GRADUATE SCHOOL', 'ETEEAP', 'PALAESTRA', 'PQA', 'CDO', 'COECS', 'COECS LAB', 'LIBRARY', 'CAM LAB', 'CAM ', 'CITHM', 'SINSAI', 'OLIVE', 'BOOKSTORE', 'CULINARY', 'TESDA']
        for department in departments:
            new_department = Department(department=department)
            db.session.add(new_department)
        db.session.commit()
        print('...Done')

############################
# FLASK ENDPOINTS
############################

@app.route('/', methods=['GET'])
def index():
    return redirect('/qr')

# returns a generated QR code
# note: {department} query parameter is required
@app.route('/qr', methods=['GET'])
def qr():
    args = request.args.to_dict()

    department = args.get('department')
    if department is None:
        department = ''

    all_departments = Department.query.all()
    return render_template('qr.html',
                            url=base_url,
                            departments=all_departments,
                            department=department,
                            app_title=app_title)

# returns a feedback form
@app.route('/feedback', methods=['GET', 'POST'])
def feedback():
    missing_rating = False
    missing_department = False
    if request.method == 'POST':
        department = request.form['department']
        message = request.form['message']
        rating = request.form['rating']

        if rating == '0':
            missing_rating = True

        if department == '':
            missing_department = True

        if not missing_department and not missing_rating:
            department = Department.query.filter_by(department=department).first()

            if department is None:
                print('Department not found!')
                return render_template('error.html', app_title=app_title)

            new_feedback = Feedback(message=message, rating=rating, department_id=department.id)
            db.session.add(new_feedback)
            db.session.commit()
            return redirect('/thank-you')

    # get department
    args = request.args.to_dict()
    department_arg = args.get('department')

    # verify whether provided department is valid
    if department_arg is None:
        return render_template('404.html', app_title=app_title)

    department = Department.query.filter_by(department=department_arg).first()
    if department is None:
        return render_template('404.html', app_title=app_title)

    return render_template('feedback.html',
            url=base_url,
            department=department_arg,
            app_title=app_title,
            status=[missing_department, missing_rating]
    )

# returns a feedback form
@app.route('/thank-you', methods=['GET'])
def thankyou():
    return render_template('thank-you.html', app_title=app_title)

# returns all feedbacks
@app.route('/review-feedback', methods=['GET'])
def review_feedback():
    all_feedbacks = db.session.query(
        Feedback.id,
        Feedback.rating,
        Feedback.message,
        Department.department,
        Feedback.date_created
    ).join(Department).all()
    return render_template('review-feedback.html', feedbacks=all_feedbacks, app_title=app_title)

# return all departments
@app.route('/departments', methods=['GET'])
@cross_origin()
def get_departments():
    all_departments = Department.query.all()
    result = departments_schema.dump(all_departments)
    return jsonify(result)


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=81, debug=True)
