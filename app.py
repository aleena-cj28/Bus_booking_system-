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

        sql = """ INSERT INTO users(username, password) VALUES(%s, %s) """

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

        sql=""" SELECT * FROM users WHERE username=%s AND password=%s """

        values = (username,password)
        cursor.execute(sql, values)
        user = cursor.fetchone()


        

        if user:
            return redirect("/view_buses")
        elif  username == "admin" and password == "admin222":
            return redirect("/admin_dashboard")
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

        
        check_sql ="SELECT * FROM buses WHERE bus_number=%s"
        cursor.execute(check_sql,(bus_number,))
        bus = cursor.fetchall()

        if bus:
            return "Already Added"

        sql="""INSERT INTO buses(bus_number,bus_name,source,destination,seats,available_seats)VALUES(%s,%s,%s,%s,%s,%s)"""

        values = (bus_number,bus_name,source,destination,seats,seats)
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

       
    sql = "SELECT seats FROM buses WHERE bus_number=%s"
    cursor.execute(sql,(bus_number,))
    bus = cursor.fetchone()
    available_seats=bus[0]


    select_sql="SELECT seat_number FROM booking WHERE bus_number=%s"
    cursor.execute(select_sql,(bus_number,))
    booked_seat= cursor.fetchall()
     

    booked_seat_list=[int(seat_number[0]) for seat_number in booked_seat ]

    available_seat_numbers = [
        i for i in range(1,available_seats + 1)
        if i not in booked_seat_list
        ]

    
    if request.method == "POST":

        
        userame = request.form["username"]
        seat_number = int(request.form["seat_number"])

        if seat_number in booked_seat_list:
            return "This Seat is already booked"


        insert_sql = """ INSERT INTO booking(username,bus_number,seat_number) VALUES(%s, %s, %s) """
        values=(userame,bus_number,seat_number)
        cursor.execute(insert_sql,values) 

        update_sql = """ UPDATE buses SET available_seats=available_seats-1 WHERE bus_number=%s """
        cursor.execute(update_sql,(bus_number,))

        
        mydb.commit()

        return "seat booked"
       
            
    return render_template("book_bus.html", bus_number=bus_number,available_seats=available_seats,available_seat_numbers=available_seat_numbers)


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

