import os
from flask import Flask, render_template, url_for, request, redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
#from sqlalchemy import ForeignKey

basedir = os.path.abspath(os.path.dirname(__file__))
app = Flask(__name__)
#app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///russia_database.db'
app.config['SQLALCHEMY_DATABASE_URI'] =\
        'sqlite:///' + os.path.join(basedir, 'russia_database.db')
db = SQLAlchemy(app)

class Ticket(db.Model):
    ticket_id = db.Column(db.Integer, primary_key=True)
    event_name = db.Column(db.String(300), nullable=False)
    event_timestamp = db.Column(db.DateTime(), nullable=False)
    event_location = db.Column(db.String(300), nullable=False)
    event_type = db.Column(db.String(100), nullable=False)
    price = db.Column(db.Float, nullable=False)
    barcode = db.Column(db.String(500), nullable=False)
    status = db.Column(db.String(100), nullable=False) # new, bought, outdated, canceled

class User(db.Model):
    user_id = db.Column(db.Integer, primary_key=True)
    name  = db.Column(db.String(100), nullable=False)
    phone = db.Column(db.String(20), nullable=False)

class Transaction(db.Model):
    transaction_id =db.Column(db.Integer, primary_key=True)
    seller_id = db.Column(db.Integer, db.ForeignKey(User.user_id))
    purchaser_id = db.Column(db.Integer, db.ForeignKey(User.user_id))
    ticket_id = db.Column(db.Integer, db.ForeignKey(Ticket.ticket_id))

@app.route('/')
@app.route('/home')
def main_page():
    tickets = Ticket.query.all()
    return render_template("ticket_list_page.html", tickets=tickets)

@app.route('/ticket-for-sale', methods=['POST', 'GET'])
def add_ticket():
    if request.method == "POST":
        event_name = request.form['event-name']
        event_datetime = request.form['event-datetime']
        event_city = request.form['event-city']
        event_type = request.form['event-type']
        ticket_price = request.form['price']
        ticket_barcode = request.form['barcode']

        if(bool(event_name) & bool(event_datetime) & bool(event_city) & bool(event_type) & bool(ticket_price) & bool(ticket_barcode)):
            event_datetime_obj = datetime.strptime(event_datetime, '%Y-%m-%dT%H:%M')
            event_timestamp = event_datetime_obj.strftime('%Y-%m-%d %H:%M:00')

            ticket = Ticket(event_name=event_name, 
                            event_timestamp=event_timestamp, 
                            event_location=event_city,
                            event_type=event_type,
                            price=ticket_price,
                            barcode=ticket_barcode,
                            status='new')
            try:
                db.session.add(ticket)
                db.session.commit()
                return redirect('/')
            except:
                return redirect('/failure-while-adding')
        else:
            return redirect('/ticket-for-sale')

    else:
        return render_template("add_ticket.html")

#@app.route('/profile/<string:name>/<int:id>')
@app.route('/profile')
def profile():
    return render_template("profile_page.html")

@app.route('/failure-while-adding')
def failure_while_adding():
    return render_template("failure_while_adding.html")

if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    app.run(debug=True)
