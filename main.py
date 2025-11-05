
import os
from flask_mysqldb import MySQL
from flask import Flask, render_template, request, redirect, url_for, flash, session, jsonify
import mysql.connector
from werkzeug.security import generate_password_hash, check_password_hash
from dotenv import load_dotenv
from flask import request, render_template, redirect, url_for, flash
from werkzeug.security import generate_password_hash





# Load env file (name it .env or database.env; adjust path if needed)
load_dotenv("database.env")

app = Flask(__name__)
app.secret_key = os.getenv("SECRET_KEY", "dev-secret")
#mysql = MySQL(app)
#cursor = mysql.connection.cursor()

# DB helper
def get_db_connection():
    return mysql.connector.connect(
        host=os.getenv("MYSQL_HOST"),
        user=os.getenv("MYSQL_USER"),
        password=os.getenv("MYSQL_PASSWORD"),
        database=os.getenv("MYSQL_DATABASE"),
        auth_plugin="mysql_native_password"
    )




# ---------------- Home  --------------------------------
@app.route("/")
def home():
    return render_template("home.html")




# --------------------------------organization signup-------------------------

@app.route("/organization/signup", methods=["GET", "POST"])
def organization_signup():
    if request.method == "GET":
        return render_template("organization_signup.html")

    name = request.form["organizationName"]
    person = request.form["contactPerson"]
    email = request.form["email"]
    phone = request.form["phone"]
    address = request.form["address"]
    pwd = request.form["password"]

    password_hash = generate_password_hash(pwd)

    conn = get_db_connection()
    c = conn.cursor()

    c.execute("""
        INSERT INTO organizations (organization_name, contact_person, email, phone, address, password_hash) 
        VALUES (%s, %s, %s, %s, %s, %s)
    """, (name, person, email, phone, address, password_hash))

    conn.commit()
    conn.close()

    flash("Signup successful! Please login.", "success")
    return redirect(url_for('organization_login'))





#-------------------------------organization login ----------------------------------------------------



@app.route("/organization/login", methods=["GET", "POST"])
def organization_login():
    if request.method == "GET":
        return render_template("organization_login.html")

    email_phone = request.form.get("email_phone").strip()
    pwd = request.form.get("organizationPassword").strip()

    # Backend validation
    if not email_phone or not pwd:
        flash("All fields are required!", "error")
        return redirect(url_for("organization_login"))
# Validate only when input looks like phone number
    if email_phone.isdigit() and len(email_phone) != 10:
        flash("Phone number must be 10 digits", "error")
        return redirect(url_for("organization_login"))


    conn = get_db_connection()
    cur = conn.cursor(dictionary=True)
    #cur.execute("SELECT * FROM organizations WHERE phone=%s", (email_phone,))
    cur.execute("""
        SELECT * FROM organizations 
        WHERE email=%s OR phone=%s
    """, (email_phone, email_phone))
    o = cur.fetchone()
    cur.close()
    conn.close()

    # Validate user
    if not o or not check_password_hash(o["password_hash"], pwd):
        flash("Invalid mobile or password", "error")
        return redirect(url_for("organization_login"))

    # Set session
    session["organization_id"] = o["id"]
    session["organization_name"] = o["organization_name"]

    return redirect(url_for("organization_myactivities"))



#-------------------------organization posting activity--------------------


@app.route("/organization/post", methods=["GET", "POST"])
def organization_post():
    if request.method == "GET":
        return render_template("organization_post.html")

    org_id = session.get("organization_id")
    org_name = session.get("organization_name")

    if not org_id:
        return redirect(url_for("organization_login"))

    data = (
        org_id,
        org_name,
        request.form["activity_name"],
        request.form["purpose"],
        request.form["activity_date"],
        request.form["activity_time"],
        request.form["address"],
        request.form["volunteers_required"],
        request.form["volunteers_skills"],
        request.form["contact"]
    )

    conn = get_db_connection()
    c = conn.cursor()
    c.execute("""
        INSERT INTO activities
        (organization_id, organization_name, activity_name, purpose, activity_date, activity_time, address, volunteers_required, volunteer_skills, contact)
        VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)
    """, data)
    
    conn.commit()
    conn.close()

    return redirect(url_for("organization_myactivities"))


#------------------------ organization myactivities -------------


@app.route("/organization/myactivities")
def organization_myactivities():
    if "organization_id" not in session:
        return redirect(url_for("organization_login"))

    org_id = session["organization_id"]

    conn = get_db_connection()
    c = conn.cursor(dictionary=True)
    c.execute("""
        SELECT * FROM activities 
        WHERE organization_id = %s 
        ORDER BY id DESC
    """, (org_id,))
    
    activities = c.fetchall()
    conn.close()

    return render_template("organization_myactivities.html", activities=activities)



#-----------------------organization  activity updates----------------


@app.route("/organization/update_activity/<int:id>", methods=["POST"])
def update_activity(id):
    if "organization_id" not in session:
        return redirect(url_for("organization_login"))

    name = request.form.get("activity_name")
    purpose = request.form.get("purpose")
    date = request.form.get("activity_date")
    time = request.form.get("activity_time")
    address = request.form.get("address")
    volunteers = request.form.get("volunteers_required")
    skills = request.form.get("volunteer_skills")
    contact = request.form.get("contact")

    conn = get_db_connection()
    cur = conn.cursor()

    cur.execute("""
        UPDATE activities
        SET activity_name=%s, purpose=%s, activity_date=%s, activity_time=%s,
            address=%s, volunteers_required=%s, volunteer_skills=%s, contact=%s
        WHERE id=%s
    """, (name, purpose, date, time, address, volunteers, skills, contact, id))

    conn.commit()
    cur.close()
    conn.close()

    return redirect(url_for("organization_myactivities"))


#-------------------organization  activity delete--------------------




@app.route("/organization/delete/<int:id>")
def delete_activity(id):
    conn = get_db_connection()
    c = conn.cursor()
    c.execute("DELETE FROM activities WHERE id=%s", (id,))
    conn.commit()
    conn.close()
    return redirect(url_for("organization_myactivities"))



#------------------------------------ organization request -----------------


@app.route("/organization/requests")
def organization_requests():
    if "organization_id" not in session:
        flash("Please login first.", "error")
        return redirect(url_for("organization_login"))

    org_id = session["organization_id"]
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    cursor.execute("""
    SELECT r.id AS req_id, r.status, 
           v.id AS volunteer_id, v.full_name, v.phone, v.email, v.skills, 
           a.activity_name, a.id AS activity_id
    FROM volunteer_activity_requests r
    JOIN volunteers v ON r.volunteer_id = v.id
    JOIN activities a ON r.activity_id = a.id
    WHERE a.organization_id = %s
    ORDER BY r.created_at DESC
""", (org_id,))


    requests = cursor.fetchall()
    cursor.close()
    conn.close()

    return render_template("organization_requests.html", requests=requests)

#--------------------------- organiation approve -----------------------------------------------

@app.route('/organization/approve/<int:req_id>')
def organization_approve(req_id):
    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute("UPDATE volunteer_activity_requests SET status='approved' WHERE id=%s", (req_id,))
    conn.commit()

    cursor.close()
    conn.close()

    flash("Volunteer approved!", "success")
    return redirect(url_for('organization_requests'))



#---------------------------- organization reject --------------------------------------------------


@app.route('/organization/reject/<int:req_id>')
def organization_reject(req_id):
    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute("UPDATE volunteer_activity_requests SET status='rejected' WHERE id=%s", (req_id,))
    conn.commit()

    cursor.close()
    conn.close()

    flash("Volunteer rejected!", "info")
    return redirect(url_for('organization_requests'))








############################################### volunteer signup ##########################

@app.route("/volunteer/signup", methods=["GET", "POST"])
def volunteer_signup():
    if request.method == "GET":
        return render_template("volunteer_signup.html")

    full_name = request.form.get("full_name", "").strip()
    email = request.form.get("email", "").strip()
    phone = request.form.get("phone", "").strip()
    skills = request.form.get("skills", "").strip()
    password = request.form.get("password", "").strip()

    hashed_password = generate_password_hash(password)

    conn = get_db_connection()
    c = conn.cursor()

    c.execute("""
        INSERT INTO volunteers (full_name, email, phone, skills, password_hash)
        VALUES (%s, %s, %s, %s, %s)
    """, (full_name, email, phone, skills, hashed_password))

    conn.commit()
    conn.close()

    return redirect(url_for("volunteer_login"))






#################################################  volunteer login  #############################################


@app.route("/volunteer/login", methods=["GET", "POST"])
def volunteer_login():
    if request.method == "GET":
        return render_template("volunteer_login.html")

    email_phone = request.form.get("email_phone", "").strip()
    password = request.form.get("password", "").strip()

    conn = get_db_connection()
    c = conn.cursor(dictionary=True)

    # Login using either email or phone
    c.execute("""
        SELECT * FROM volunteers 
        WHERE email=%s OR phone=%s
    """, (email_phone, email_phone))

    volunteer = c.fetchone()
    conn.close()

    if not volunteer or not check_password_hash(volunteer["password_hash"], password):
        flash("Invalid login credentials!", "error")
        return redirect(url_for("volunteer_login"))

    # Save user session
    session["volunteer_id"] = volunteer["id"]
    session["volunteer_name"] = volunteer["full_name"]

    return redirect(url_for("volunteer_activities"))



##################################################### volunteer activities posted  ########################################


@app.route('/volunteer/activities')
def volunteer_activities():
    if 'volunteer_id' not in session:
        flash("Please login first.", "error")
        return redirect(url_for('volunteer_login'))

    volunteer_id = session['volunteer_id']
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    cursor.execute("""
        SELECT 
            a.*, 
            o.organization_name, 
            o.contact_person,
            o.phone AS contact,
            o.address AS address,
            COALESCE(
                (SELECT status FROM volunteer_activity_requests 
                 WHERE volunteer_id=%s AND activity_id=a.id LIMIT 1),
                'none'
            ) AS req_status
        FROM activities a
        JOIN organizations o ON a.organization_id = o.id
        ORDER BY a.activity_date
    """, (volunteer_id,))

    activities = cursor.fetchall()
    cursor.close()
    conn.close()

    return render_template('volunteer_activities.html', activities=activities)


###################################### volunteer join activities #########################################################



@app.route('/volunteer/join/<int:activity_id>', methods=["POST"])
def volunteer_join_activity(activity_id):
    if 'volunteer_id' not in session:
        flash("Please login first.", "error")
        return redirect(url_for('volunteer_login'))

    volunteer_id = session["volunteer_id"]

    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    # Check already exists
    cursor.execute("""
        SELECT * FROM volunteer_activity_requests
        WHERE volunteer_id=%s AND activity_id=%s
    """, (volunteer_id, activity_id))

    existing = cursor.fetchone()

    if existing:
        flash("You already requested to join this activity.", "warning")
        cursor.close()
        conn.close()
        return redirect(url_for("volunteer_activities"))

    cursor.execute("""
        INSERT INTO volunteer_activity_requests (volunteer_id, activity_id, status)
        VALUES (%s, %s, 'pending')
    """, (volunteer_id, activity_id))

    conn.commit()
    cursor.close()
    conn.close()

    flash("Request sent! Waiting for organization approval.", "success")
    return redirect(url_for("volunteer_activities"))




########################################### volunteer joined activities  ###############################


@app.route("/volunteer/myactivities")
def volunteer_myactivities():
    if "volunteer_id" not in session:
        flash("Please login first.", "error")
        return redirect(url_for("volunteer_login"))

    volunteer_id = session["volunteer_id"]

    conn = get_db_connection()
    cur = conn.cursor(dictionary=True)

    cur.execute("""
        SELECT a.*, r.status
        FROM volunteer_activity_requests r
        JOIN activities a ON r.activity_id = a.id
        WHERE r.volunteer_id = %s
        ORDER BY a.activity_date
    """, (volunteer_id,))

    activities = cur.fetchall()
    cur.close()
    conn.close()

    return render_template("volunteer_myactivities.html", activities=activities)



##################################### volunteer leave activity #########################################


@app.route('/volunteer/leave/<int:activity_id>', methods=['POST'])
def volunteer_leave_activity(activity_id):
    if "volunteer_id" not in session:
        flash("Please login first.", "error")
        return redirect(url_for("volunteer_login"))

    volunteer_id = session["volunteer_id"]

    conn = get_db_connection()
    cur = conn.cursor()

    # Delete request from request table
    cur.execute("""
        DELETE FROM volunteer_activity_requests
        WHERE volunteer_id = %s AND activity_id = %s
    """, (volunteer_id, activity_id))

    conn.commit()
    cur.close()
    conn.close()

    flash("You left the activity successfully!", "success")
    return redirect(url_for('volunteer_myactivities'))






#----------------------------volunteer join activity---------------------------------------


@app.route("/join_activity/<int:activity_id>", methods=["POST"])
def join_activity(activity_id):
    volunteer_id = session.get("volunteer_id")

    conn = get_db_connection()
    c = conn.cursor()
    c.execute("""
        INSERT INTO activity_requests (activity_id, volunteer_id, status)
        VALUES (%s, %s, 'pending')
    """, (activity_id, volunteer_id))
    conn.commit()
    conn.close()

    return redirect(url_for("volunteer_dashboard"))


from waitress import serve

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))  # Render uses PORT env
    app.run(host="0.0.0.0", port=port)
