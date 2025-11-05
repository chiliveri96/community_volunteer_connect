
import os
from flask_mysqldb import MySQL
from flask import Flask, render_template, request, redirect, url_for, flash, session, jsonify
import mysql.connector
from werkzeug.security import generate_password_hash, check_password_hash
from dotenv import load_dotenv



# Load env file (name it .env or database.env; adjust path if needed)
load_dotenv("database.env")

app = Flask(__name__)
app.secret_key = os.getenv("SECRET_KEY", "dev-secret")
#mysql = MySQL(app)
#cursor = mysql.connection.cursor()

# DB helper
def get_db_connection():
    return mysql.connector.connect(
        host=os.getenv("MYSQL_HOST", "cvc-db-abcde.render.com"),
        user=os.getenv("MYSQL_USER", "root"),
        password=os.getenv("MYSQL_PASSWORD", ""),
        database=os.getenv("MYSQL_DATABASE", "community_volunteer_connect"),
        auth_plugin="mysql_native_password"
    )

# Home
@app.route("/")
def home():
    return render_template("home.html")

# volunteerunteer signup
@app.route("/volunteer/signup", methods=["GET", "POST"])
def volunteer_signup():
    if request.method == "GET":
        return render_template("volunteer_signup.html")

    first_name = request.form.get("firstName", "").strip()
    last_name = request.form.get("lastName", "").strip()
    phone = request.form.get("phone", "").strip()
    email = request.form.get("email", "").strip().lower()
    password = request.form.get("password", "")

    if not all([first_name, last_name, phone, email, password]):
        flash("All fields are required.", "error")
        return redirect(url_for("volunteer_signup"))
    if not phone.isdigit() or len(phone) != 10:
        flash("Phone must be a 10-digit number.", "error")
        return redirect(url_for("volunteer_signup"))
    if len(password) < 6:
        flash("Password must be at least 6 characters.", "error")
        return redirect(url_for("volunteer_signup"))

    password_hash = generate_password_hash(password)

    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT id FROM volunteers WHERE email=%s OR phone=%s", (email, phone))
    if cursor.fetchone():
        cursor.close()
        conn.close()
        flash("Email or phone already registered.", "error")
        return redirect(url_for("volunteer_signup"))

    cursor.execute(
        "INSERT INTO volunteers (first_name, last_name, email, phone, password_hash) VALUES (%s,%s,%s,%s,%s)",
        (first_name, last_name, email, phone, password_hash)
    )
    conn.commit()
    cursor.close()
    conn.close()
    flash("Signup successful — please login.", "success")
    return redirect(url_for("volunteer_login"))

# volunteerunteer login
@app.route("/volunteer/login", methods=["GET", "POST"])
def volunteer_login():
    if request.method == "GET":
        return render_template("volunteer_login.html")
    phone = request.form.get("phone", "").strip()
    password = request.form.get("password", "").strip()
    if not phone or not password:
        flash("All fields required.", "error")
        return redirect(url_for("volunteer_login"))

    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM volunteers WHERE phone=%s AND status='active'", (phone,))
    user = cursor.fetchone()
    cursor.close()
    conn.close()

    if not user or not check_password_hash(user["password_hash"], password):
        flash("Invalid credentials", "error")
        return redirect(url_for("volunteer_login"))

    session["volunteer_id"] = user["id"]
    session["volunteer_name"] = user["first_name"]
    flash(f"Welcome {user['first_name']}", "success")
    return redirect(url_for("volunteer_activities"))




@app.route('/volunteer/activities', methods=['GET'])
def volunteer_activities():
    if 'volunteer_id' not in session:
        flash("Please login first.", "error")
        return redirect(url_for('volunteer_login'))

    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM activities")
    activities = cursor.fetchall()
    cursor.close()
    conn.close()

    return render_template('volunteer_activities.html', activities=activities)



@app.route('/volunteer/join/<int:activity_id>', methods=['POST'])
def volunteer_join_activity(activity_id):
    if 'volunteer_id' not in session:
        flash("Please login first.", "error")
        return redirect(url_for('volunteer_login'))

    volunteer_id = session['volunteer_id']
    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT * FROM volunteer_activities
        WHERE volunteer_id = %s AND activity_id = %s
    """, (volunteer_id, activity_id))
    already_joined = cursor.fetchone()

    if not already_joined:
        cursor.execute("""
            INSERT INTO volunteer_activities (volunteer_id, activity_id)
            VALUES (%s, %s)
        """, (volunteer_id, activity_id))
        conn.commit()
        flash("You have joined the activity successfully!", "success")
    else:
        flash("You have already joined this activity.", "warning")

    cursor.close()
    conn.close()

    return redirect(url_for('volunteer_myactivities'))



@app.route('/volunteer/myactivities', methods=['GET'])
def volunteer_myactivities():
    if 'volunteer_id' not in session:
        flash("Please login first.", "error")
        return redirect(url_for('volunteer_login'))

    volunteer_id = session['volunteer_id']
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    cursor.execute("""
        SELECT a.* FROM activities a
        JOIN volunteer_activities va ON a.id = va.activity_id
        WHERE va.volunteer_id = %s
    """, (volunteer_id
,))
    activities = cursor.fetchall()

    cursor.close()
    conn.close()

    return render_template('volunteer_myactivities.html', activities=activities)



@app.route('/volunter/leave/<int:activity_id>', methods=['POST'])
def volunteer_leave_activity(activity_id):
    if 'volunteer_id' not in session:
        flash("Please login first.", "error")
        return redirect(url_for('volunteer_login'))

    volunteer_id = session['volunteer_id']
    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute("""
        DELETE FROM volunteer_activities
        WHERE volunteer_id = %s AND activity_id = %s
    """, (volunteer_id, activity_id))
    conn.commit()

    cursor.close()
    conn.close()

    flash("You have left the activity.", "info")
    return redirect(url_for('volunteer_myactivities'))





@app.route('/volunteer/join/<int:activity_id>', methods=['POST'])
def volunteer_join(activity_id):
    if 'volunteer_id' not in session:
        return redirect('/volunteer/login')

    volunteer_id= session['volunteer_id']
    conn = mysql.connect()
    c = conn.cursor()

    c.execute("INSERT INTO activity_requests(activity_id, volunteer_id) VALUES (%s, %s)",
              (activity_id, volunteer_id))
    conn.commit()
    conn.close()
    return redirect('/volunteer/myactivities')

@app.route('/organization/requests')
def organization_requests():
    if 'organization_id' not in session:
        return redirect('/login')

    organization_id = session['organization_id']

    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    cursor.execute("SELECT * FROM activity_requests WHERE organization_id=%s AND status='Pending'", (organization_id,))
    requests = cursor.fetchall()

    cursor.close()
    conn.close()

    return render_template("organization_requests.html", requests=requests)


@app.route('/join_activity/<int:activity_id>/<int:organization_id>', methods=['POST'])
def join_activity(activity_id, organization_id):
    if 'volunteer_id' not in session:
        return redirect('/volunteer/login')

    volunteer_id = session['volunteer_id']
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    # volunteerunteer details
    cursor.execute("SELECT first_name, last_name, email, phone FROM volunteers WHERE id=%s", (volunteer_id,))
    volunteer = cursor.fetchone()
    full_name = volunteer['first_name'] + " " + volunteer['last_name']

    # Activity name
    cursor.execute("SELECT activity_name FROM activities WHERE id=%s", (activity_id,))
    act = cursor.fetchone()

    # Insert request
    cursor.execute("""
        INSERT INTO activity_requests (volunteer_id, organization_id, activity_id, volunteer_name, email, phone, activity_name, status)
        VALUES (%s, %s, %s, %s, %s, %s, %s, 'Pending')
    """, (volunteer_id, organization_id, activity_id, full_name, volunteer['email'], volunteer['phone'], act['activity_name']))

    conn.commit()
    cursor.close()
    conn.close()

    return redirect('/volunteer/myactivities')












# -------------------- organization-------------------

@app.route("/organization/signup", methods=["GET","POST"])
def organization_signup():
    if request.method=="GET":
        return render_template("organization_signup.html")

    name = request.form["organizationName"]
    person = request.form["contactPerson"]
    email = request.form["email"]
    phone = request.form["phone"]
    address = request.form["address"]
    pwd = request.form["password"]

    hash = generate_password_hash(pwd)

    conn = get_db_connection()
    c = conn.cursor()
    c.execute("INSERT INTO organization(organization_name,contact_person,email,phone,address,password_hash) VALUES (%s,%s,%s,%s,%s,%s)",
              (name,person,email,phone,address,hash))
    conn.commit()
    conn.close()
    return redirect(url_for("organization_login"))

@app.route("/organization/login", methods=["GET","POST"])
def organization_login():
    if request.method=="GET":
        return render_template("organization_login.html")

    phone = request.form["organizationPhone"]
    pwd = request.form["organizationPassword"]

    conn = get_db_connection()
    c = conn.cursor(dictionary=True)
    c.execute("SELECT * FROM organization WHERE phone=%s",(phone,))
    o = c.fetchone()
    conn.close()

    if not o or not check_password_hash(o["password_hash"], pwd):
        flash("Invalid login","error")
        return redirect(url_for("organization_login"))

    session["organization_id"]=o["id"]
    session["organization_name"]=o["organization_name"]

    return redirect(url_for("organization_myactivities"))

@app.route("/organization/post", methods=["GET", "POST"])
def organization_post():
    if request.method == "GET":
        return render_template("organization_post.html")

    data = (
        session["organization_id"],
        session["organization_name"],
        request.form["activity_name"],
        request.form["purpose"],
        request.form["activity_date"],
        request.form["activity_time"],
        request.form["address"],
        request.form["volunteer_required"],
        request.form["category"],
        request.form["contact"]
    )

    conn = get_db_connection()
    c = conn.cursor()
    c.execute("""
        INSERT INTO activities
        (organization_id, organization_name, activity_name, purpose, activity_date, activity_time, address, volunteerunteers_required, category, contact)
        VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)
    """, data)
    conn.commit()
    conn.close()

    return redirect(url_for("organization_myactivities"))


@app.route("/organization/myactivities")
def organization_myactivities():
    oid = session["organization_id"]
    conn = get_db_connection()
    c = conn.cursor(dictionary=True)
    c.execute("SELECT * FROM activities WHERE organization_id=%s ORDER BY id DESC", (oid,))
    data = c.fetchall()
    conn.close()
    return render_template("organization_myactivities.html", activities=data)


@app.route('/organization/update/<int:id>', methods=['POST'])
def update_activity(id):
    data = (
        request.form['activity_name'],
        request.form['purpose'],
        request.form['activity_date'],
        request.form['address'],
        id
    )

    conn = get_db_connection()
    c = conn.cursor()
    c.execute("""
        UPDATE activities 
        SET activity_name=%s, purpose=%s, activity_date=%s, address=%s 
        WHERE id=%s
    """, data)
    conn.commit()
    conn.close()
    
    
    
    
@app.route("/organization/request/accept/<int:req_id>")
def organization_accept(req_id):
    conn = get_db_connection()
    c = conn.cursor()
    
    # Move request to volunteerunteer_activities table
    c.execute("""
        INSERT INTO volunteer_activities (volunteer_id, activity_id)
        SELECT volunteer_id, activity_id FROM activity_requests WHERE id=%s
    """,(req_id,))

    # Delete request from activity_requests
    c.execute("DELETE FROM activity_requests WHERE id=%s", (req_id,))
    
    conn.commit()
    conn.close()
    
    return redirect("/organization/requests")


@app.route("/organization/request/reject/<int:req_id>")
def organization_reject(req_id):
    conn = get_db_connection()
    c = conn.cursor()
    c.execute("DELETE FROM activity_requests WHERE id=%s", (req_id,))
    conn.commit()
    conn.close()
    
    return redirect("/organization/requests")


@app.route('/organization/request/accept/<int:req_id>', methods=['POST'])
def accept_request(req_id):
   conn = get_db_connection()
   c = conn.cursor(dictionary=True)
   c.execute("UPDATE activity_requests SET status='accepted' WHERE id=%s", (req_id,))
   conn.commit()
   conn.close()
   return redirect('/organization/requests')


@app.route('/organization/request/reject/<int:req_id>', methods=['POST'])
def reject_request(req_id):
    conn = mysql.connect()
    c = conn.cursor()
    c.execute("UPDATE activity_requests SET status='rejected' WHERE id=%s", (req_id,))
    conn.commit()
    conn.close()
    return redirect('/organization/requests')
    return redirect(url_for('organization_myactivities'))


@app.route('/organization/delete/<int:id>')
def delete_activity(id):
    conn = get_db_connection()
    c = conn.cursor()
    c.execute("DELETE FROM activities WHERE id=%s", (id,))
    conn.commit()
    conn.close()
    return redirect(url_for('organization_myactivities'))

    
if __name__ == "__main__":
    app.run(debug=True)
