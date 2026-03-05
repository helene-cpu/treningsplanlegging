from flask import Flask, render_template, redirect, session
import mysql.connector
from forms import RegisterForm, LoginForm

app = Flask(__name__)
app.secret_key = "veldig_hemmelig"

def get_conn():
    return mysql.connector.connect(
        host="localhost",
        user="trening",
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
            "SELECT navn FROM Brukere WHERE brukernavn=%s AND passord=%s",
            (brukernavn, password)
        )

        user = cur.fetchone()

        cur.close()
        conn.close()

        if user:
            session['navn'] = user[0]
            return redirect("/dashboard")
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

        conn = get_conn()
        cur = conn.cursor()

        cur.execute(
            "INSERT INTO Brukere (Navn, Brukernavn, Passord) VALUES (%s, %s, %s)",
            (navn, brukernavn, passord)
        )

        conn.commit()
        cur.close()
        conn.close()

        return redirect("/")

    return render_template("register.html", form=form)

@app.route("/dashboard", methods=["POST", "GET"])
def dashboard():
    return render_template("dashboard.html")


if __name__ == "__main__":
    app.run(debug=True)