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

current_seat_number = 2100

@app.route("/")
def home():
    return render_template("home.html")

class Passenger(db.Model):
    __tablename__ = "passengers"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(40))
    number = db.Column(db.Integer)
    from_dest = db.Column(db.String(40))
    to_dest = db.Column(db.String(40))
    p_class = db.Column(db.String(40))
    seats = db.Column(db.Integer)
    airways = db.Column(db.String(40))
    flight_n= db.Column(db.Integer)
    seat_no = db.Column(db.Integer)
    dt = db.Column(db.Date)
    brdng = db.Column(db.String(40))
  

    def __init__(self, name, number, fromstation, tostation, p_class, seats, airways, flight_n, seat_no, dt, brdng):
        self.name = name
        self.number = number
        self.from_dest = fromstation
        self.to_dest = tostation  
        self.p_class = p_class  
        self.seats = seats
        self.airways = airways
        self.flight_n = flight_n
        self.seat_no = seat_no
        self.dt = dt
        self.brdng = brdng
        

@app.route("/", methods=["post"])
def test():
    avl = request.form.get("input_fld")
    frm = request.form.get("origin")

    result = "a"

    if avl and frm:
        cursor.execute(
            "SELECT * from planes WHERE destination ILIKE %s AND origin ILIKE %s AND avail_seats > 0  ORDER BY plane_no ASC",(avl,frm,),)
        result = cursor.fetchall()
    elif avl:
        cursor.execute("SELECT * from planes WHERE destination ILIKE %s AND avail_seats > 0 ORDER BY plane_no ASC",(avl,),)
        result = cursor.fetchall()
    elif frm:
        cursor.execute("SELECT * from planes WHERE origin ILIKE %s AND avail_seats > 0 ORDER BY plane_no ASC", (frm,))
        result = cursor.fetchall()
    else:
        result = ""

    pname = request.form.get("p_name")
    plnno = request.form.get("a_no")
    details =""
    if pname and plnno:
        cursor.execute("select * from passengers where name ILIKE %s and flight_n = %s",(pname, plnno,),)
        details = cursor.fetchall()    
    elif pname :
        cursor.execute("select * from passengers where name ILIKE %s ",(pname,),)
        details = cursor.fetchall()
    elif plnno:
        cursor.execute("select * from passengers where flight_n = %s",(plnno,),)
        details = cursor.fetchall()

    cursor.execute("SELECT * FROM planes ORDER BY plane_no ASC")
    all = cursor.fetchall()

    if request.method == "POST":

        if "booking" in request.form:
            msg = " "
            return render_template("searchplanes.html", msg=msg)

        if request.method == "POST":
            session["input_fld"] = request.form.get("input_fld")
            session["origin"] = request.form.get("origin")
        else:
            session.setdefault = ("input_fld", "")
            session.setdefault = ("origin", "")

        if "t_cancel" in request.form:
            abc =""
            return render_template("ticket_cancellation.html", abc=abc)
        elif "search_t" in request.form:
            if len(details) == 0:

                message = "TICKET NOT FOUND"
                return render_template("ticket_cancellation.html", message=message)
            else:
                return render_template("ticket_cancellation.html", data = details)
        elif "ticketcancel" in request.form:
            p_nm = request.form.get("p_nm")
            planeno = request.form.get("pl_n")
            cursor.execute("UPDATE planes SET avail_seats = avail_seats + 1 WHERE plane_no = %s ", (planeno, ),)
            con.commit()
            cursor.execute("delete from passengers where flight_n = %s and name ilike %s", (planeno, p_nm,),)
            con.commit()
            return render_template("a.html")
        

        if "ticket" in request.form:
            global current_seat_number
            
            current_seat_number += 1
            flight_n = request.form.get("flight_n")
            session["selected_number"] = flight_n
            airways = request.form.get("airways")
            session["selected_flight"] = airways
            brdng = request.form.get("brdng")
            session["selected_brdng"] = brdng
            return render_template("booking.html", brdng=brdng, airways=airways, flight_n=flight_n, seat_no=current_seat_number)
        
        if "home" in request.form:
            return render_template("home.html")

        if "trains" in request.form:
            return render_template("planeschedule.html", data=all)

        # if avl is None:

        #   return render_template ("test.html",msg=msg)
        elif "avl_trn" in request.form:

            if len(result) == 0:

                message = "FLIGHTS NOT AVAILABLE"
                return render_template("searchplanes.html", message=message)
            else:
                return render_template("searchplanes.html", data=result)
        # Get the form data
        # train_name = request.form["train_name"]
        # num_seats = request.form["seats"]
    
        # Update the available seats in the 'Trains' table
        # cursor.execute("UPDATE Trains SET avail_seats = avail_seats - %s WHERE train_name = %s",(num_seats, train_name),)
    
        # Commit the changes to the database
        
    name = request.form["name"]
    number = request.form["number"]
    from_dest = request.form["fromstation"]
    to_dest = request.form["tostation"]
    p_class = request.form["p_class"]
    seats = request.form["seats"]
    airways = request.form["airways"]
    flight_n = request.form["flight_n"] 
    seat_no = request.form["seat_no"]
    dt = request.form["dt"]
    brdng = request.form["brdng"]

    passenger = Passenger(name, number, from_dest, to_dest, p_class, seats, airways, flight_n, seat_no, dt, brdng)
    db.session.add(passenger)
    db.session.commit()

    passengerResult = db.session.query(Passenger).filter(Passenger.id == 1)
    for result in passengerResult:
        print(
            result.name,
            result.number,
            result.from_dest,
            result.to_dest,
            result.p_class,
            result.seats,
            result.airways,
            result.flight_n,
            result.seat_no,
            result.dt,
            result.brdng
        )

    plane_n=request.form.get('flight_n')    
    requested_seats= int(request.form.get('seats'))
    cursor.execute("SELECT avail_seats FROM planes WHERE plane_no = %s", (plane_n,))
   
    res = cursor.fetchone()    
    if "BOOK" in request.form:
        available_seats=res[0]
        if requested_seats <= available_seats:
         cursor.execute("UPDATE planes SET avail_seats = avail_seats - %s WHERE plane_no = %s",(requested_seats, plane_n),)
         con.commit()
         return render_template(
            "done.html", data=(name, from_dest, to_dest, dt, seat_no, airways, p_class, flight_n, brdng)
         )
        else:
            return render_template("error.html")
        
        
if __name__ == "__main__":
    app.run(debug=True)