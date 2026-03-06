from flask import Flask, render_template, redirect, session
import mysql.connector
from forms import RegisterForm, LoginForm, PlanForm
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
app.secret_key = "veldig_hemmelig"

def get_conn():
    return mysql.connector.connect(
        host="localhost",
        user="trener",
        password="Strkno321!",
        database="treningsplanlegger"
    )

@app.route('/', methods=["GET", "POST"])
def index():
    form = LoginForm()

    if form.validate_on_submit():
        brukernavn = form.username.data
        password = form.password.data

        conn = get_conn()
        cur = conn.cursor()

        cur.execute(
            "SELECT navn, passord FROM brukere WHERE Brukernavn=%s",
            (brukernavn,)
        )

        user = cur.fetchone()

        cur.close()
        conn.close()

        #sjekker om bruker eksisterer
        if user:
            passord_db = user[1]

            if check_password_hash(passord_db, password):
                session['navn'] = user[0]
                return redirect("/dashboard")
            else:
                form.username.errors.append("Feil brukernavn eller passord")

        else:
            form.username.errors.append("Feil brukernavn eller passord")

    return render_template('index.html', form=form)


@app.route("/register", methods=["GET", "POST"])
def register():
    form = RegisterForm()

    if form.validate_on_submit():

        navn = form.name.data
        brukernavn = form.username.data
        passord = form.password.data

        #lagre passord som en hash
        passord_hash = generate_password_hash(passord)

        conn = get_conn()
        cur = conn.cursor()

        cur.execute(
            "INSERT INTO brukere (Navn, Brukernavn, Passord) VALUES (%s, %s, %s)",
            (navn, brukernavn, passord_hash)
        )

        conn.commit()
        cur.close()
        conn.close()

        return redirect("/")

    return render_template("register.html", form=form)

@app.route("/dashboard", methods=["POST", "GET"])
def dashboard():
    form= PlanForm()

    aktivitet = form.aktivitet.data

    if "navn" not in session:
        return redirect("/")

    conn = get_conn()
    cur = conn.cursor()

    if form.validate_on_submit():

        cur.execute(
            "INSERT INTO treningsplan(Navn, aktivitet) VALUES (%s, %s)",
            (session["navn"], aktivitet)
        )
        conn.commit()
        cur.close()
        conn.close()

    return render_template("dashboard.html", form=form)


if __name__ == "__main__":
    app.run(debug=True)