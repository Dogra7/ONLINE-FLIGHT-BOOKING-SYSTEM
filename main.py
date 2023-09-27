import psycopg2
from flask_sqlalchemy import SQLAlchemy
from flask import Flask, request, render_template, session,jsonify
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

app = Flask(__name__)
app.secret_key = "deep"

engine = create_engine("postgresql://postgres:deep1234@localhost:5432/FLIGHT BOOKING")
Session = sessionmaker(bind=engine)

app.config["SQLALCHEMY_DATABASE_URI"] = "postgresql://postgres:deep1234@localhost:5432/FLIGHT BOOKING"

db = SQLAlchemy(app)

con = psycopg2.connect(
    database="FLIGHT BOOKING",
    user="postgres",
    password="deep1234",
    host="127.0.0.1",
    port="5432",
)
cursor = con.cursor()

@app.route("/")
def home():
    return render_template("home.html")
    #  return 'Hello, World!!!'

class Passenger(db.Model):
    __tablename__ = "Passengers"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(40))
    number = db.Column(db.Integer)
    fromstation = db.Column(db.String(40))
    tostation = db.Column(db.String(40))
    dt = db.Column(db.Date)
    seats = db.Column(db.Integer)
    train_name = db.Column(db.String(40))

    def __init__(self, name, number, fromstation, tostation, dt, seats, train_name):
        self.name = name
        self.number = number
        self.fromstation = fromstation
        self.tostation = tostation
        self.dt = dt

        self.seats = seats
        self.train_name = train_name

@app.route("/", methods=["post"])
def test():
    avl = request.form.get("input_fld")
    frm = request.form.get("origin")
    # cursor.execute("SELECT * from trains WHERE destination ILIKE %s OR origin ILIKE %s  ORDER BY train_name ASC",(avl, frm,))
    # result = cursor.fetchall()
    # cursor.execute("SELECT train_name from trains WHERE destination ILIKE %s OR origin ILIKE %s  ORDER BY train_name ASC",(avl, frm,))
    # trains = cursor.fetchall()

    result = "a"

    if avl and frm:
        cursor.execute(
            "SELECT * from planes WHERE destination ILIKE %s AND origin ILIKE %s AND avail_seats > 0  ORDER BY plane_name ASC",(avl,frm,),)
        result = cursor.fetchall()
        cursor.execute("SELECT plane_nm from planes WHERE destination ILIKE %s AND origin ILIKE %s AND avail_seats > 0  ORDER BY plane_nm ASC",(avl,frm,),)
        trains = cursor.fetchall()
    elif avl:
        cursor.execute("SELECT * from planes WHERE destination ILIKE %s AND avail_seats > 0 ORDER BY plane_no ASC",(avl,),)
        result = cursor.fetchall()
        cursor.execute("SELECT plane_nm from planes WHERE destination ILIKE %s AND avail_seats > 0", (avl,))
        trains = cursor.fetchall()
    elif frm:
        cursor.execute("SELECT * from planes WHERE origin ILIKE %s AND avail_seats > 0 ORDER BY plane_no ASC", (frm,))
        result = cursor.fetchall()
        cursor.execute("SELECT plane_nm from planes WHERE origin ILIKE %s AND avail_seats > 0", (frm,))
        trains = cursor.fetchall()
    else:
        result = ""

    cursor.execute("SELECT * FROM planes ORDER BY plane_no ASC")
    all = cursor.fetchall()
    if request.method == "POST":

        if "booking" in request.form:
            msg = " "
            return render_template("searchtrains.html", msg=msg)

        if request.method == "POST":
            session["input_fld"] = request.form.get("input_fld")
            session["origin"] = request.form.get("origin")
        else:
            session.setdefault = ("input_fld", "")
            session.setdefault = ("origin", "")

        if "ticket" in request.form:
            return render_template("booking.html", trains=trains)

        if "home" in request.form:
            return render_template("home.html")

        if "trains" in request.form:
            return render_template("trainschedule.html", data=all)

        # if avl is None:

        #   return render_template ("test.html",msg=msg)
        elif "avl_trn" in request.form:

            if len(result) == 0:

                message = "TRAINS NOT AVAILABLE"
                return render_template("searchtrains.html", message=message)
            else:
                return render_template("searchtrains.html", data=result)

        # Get the form data
        # train_name = request.form["train_name"]
        # num_seats = request.form["seats"]

        # Update the available seats in the 'Trains' table
        # cursor.execute("UPDATE Trains SET avail_seats = avail_seats - %s WHERE train_name = %s",(num_seats, train_name),)

        # Commit the changes to the database
        
    name = request.form["name"]
    number = request.form["number"]
    fromstation = request.form["fromstation"]
    tostation = request.form["tostation"]
    dt = request.form["dt"]
    seats = request.form["seats"]
    train_name = request.form["train_name"]

    passenger = Passenger(name, number, fromstation, tostation, dt, seats, train_name)
    db.session.add(passenger)
    db.session.commit()

    passengerResult = db.session.query(Passenger).filter(Passenger.id == 1)
    for result in passengerResult:
        print(
            result.name,
            result.number,
            result.fromstation,
            result.tostation,
            result.dt,
            result.seats,
            result.train_name,
        )
    train_n=request.form.get('train_name')    
    requested_seats= int(request.form.get('seats'))
    cursor.execute("SELECT avail_seats FROM trains WHERE train_name = %s", (train_n,))
    
    res = cursor.fetchone()    
    if "BOOK" in request.form:
        available_seats=res[0]
        if requested_seats <= available_seats:
         cursor.execute("UPDATE Trains SET avail_seats = avail_seats - %s WHERE train_name = %s",(requested_seats, train_n),)
         con.commit()
         return render_template(
            "done.html", data=(name, fromstation, tostation, dt, seats, train_name)
         )
        else:
            return render_template("error.html")
        
if __name__ == "__main__":
    app.run(debug=True)