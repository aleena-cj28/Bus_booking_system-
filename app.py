from flask import Flask,render_template,request,redirect
from database import mydb,cursor

app = Flask(__name__)


@app.route("/")
def home():
    return render_template("index.html")




@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":

        username = request.form["username"]
        password = request.form["password"]

        sql = """ 
        INSERT INTO users(username, password) 
        VALUES(%s, %s)
        """

        values = (username,password)
        cursor.execute(sql,values)
        mydb.commit()
        return redirect("/login")
    return render_template("register.html")




@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]

        sql="""
        SELECT * FROm users WHERE username=%s AND password=%s
        """

        values = (username,password)
        cursor.execute(sql, values)
        user = cursor.fetchone()
        if user:
            return redirect("/view_buses")
        else:
            return "Invalid Username or Password"
        
    return render_template("login.html")    





@app.route("/admin", methods=["GET", "POST"])
def admin():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]

        if username == "admin" and password == "admin222":
            return redirect("/admin_dashboard")
        else:
            return "Invalid Username or Password"
        
    return render_template("admin_login.html")



@app.route("/add_bus", methods=["GET", "POST"])
def add_bus():
    if request.method == "POST":
        bus_number = request.form["bus_number"]
        bus_name = request.form["bus_name"]
        source = request.form["source"]
        destination = request.form["destination"]
        seats = request.form["seats"]

        sql="""
        INSERT INTO buses(bus_number,bus_name,source,destination,seats)VALUES(%s,%s,%s,%s,%s)"""

        values = (bus_number,bus_name,source,destination,seats)
        cursor.execute(sql, values)
        mydb.commit()
        return "Bus Added Successfully"
    return render_template("add_bus.html")



@app.route("/view_buses")
def view_buses():

    sql= "SELECT * FROM buses"
    cursor.execute(sql)

    buses = cursor.fetchall()

    return render_template("view.html", buses=buses)





@app.route("/book_bus/<bus_number>" , methods=["GET" , "POST"])
def book_bus(bus_number):
    if request.method == "POST":
        userame = request.form["username"]
        bus_number = request.form["bus_number"] 
        seat_number = request.form["seat_number"]

        sql = """ INSERT INTO booking(username,bus_number,seat_number) VALUES(%s, %s, %s) """
    
        values=(userame,bus_number,seat_number)

        cursor.execute(sql,values)
        mydb.commit()

        return "Seat Booked"
    return render_template("book_bus.html", bus_number=bus_number)


@app.route("/admin_dashboard")
def dashboard():
    return render_template("admin_dashboard.html")



@app.route("/admin_view_buses")
def admin_view_buses():

    sql= "SELECT * FROM buses"
    cursor.execute(sql)

    bus = cursor.fetchall()

    return render_template("view_buses.html" , buses=bus)



@app.route("/view_bookings")
def view_bookings():

    sql= "SELECT * FROM booking"
    cursor.execute(sql)

    booking = cursor.fetchall()

    return render_template("view_booking.html", bookings=booking)



if __name__ == "__main__":
    app.run(debug=True)

