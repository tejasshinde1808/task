from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

# Database configuration (SQLite database)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///reminders.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# Reminder model (database table)
class Reminder(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.String(10), nullable=False)
    time = db.Column(db.String(5), nullable=False)
    message = db.Column(db.Text, nullable=False)
    remind_type = db.Column(db.String(10), nullable=False)

# API route to accept reminder data
@app.route('/api/reminder', methods=['POST'])
def create_reminder():
    data = request.json
    date = data.get('date')
    time = data.get('time')
    message = data.get('message')
    remind_type = data.get('remind_type')

    if not all([date, time, message, remind_type]):
        return jsonify({'error': 'All fields are required'}), 400

    reminder = Reminder(date=date, time=time, message=message, remind_type=remind_type)
    db.session.add(reminder)
    db.session.commit()

    return jsonify({'message': 'Reminder saved successfully'}), 201

if __name__ == '__main__':
    with app.app_context():
        db.create_all()  # Create table if not exists
    app.run(debug=True)
