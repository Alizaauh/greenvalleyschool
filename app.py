from flask import Flask, render_template, request, redirect, url_for
from flask_wtf import FlaskForm
from flask_wtf.csrf import CSRFProtect
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired, Email, Length
from flaskext.mysql import MySQL


app = Flask(__name__, template_folder="Templates", static_folder="Static")

app.config["SECRET_KEY"] = "dev-secret-key-12345"
csrf = CSRFProtect(app)

app.config["MYSQL_DATABASE_HOST"] = "localhost"
app.config["MYSQL_DATABASE_USER"] = "root"
app.config["MYSQL_DATABASE_PASSWORD"] = ""
app.config["MYSQL_DATABASE_DB"] = "admission"

mysql = MySQL(app)


class AdmissionForm(FlaskForm):
    username = StringField("Fullname", validators=[DataRequired(), Length(min=4, max=25)])
    email = StringField("Email Address", validators=[DataRequired(), Email()])
    password = PasswordField("Password", validators=[DataRequired(), Length(min=6)])
    submit = SubmitField("Register")


class LoginForm(FlaskForm):
    email = StringField("Email Address", validators=[DataRequired(), Email()])
    password = PasswordField("Password", validators=[DataRequired(), Length(min=6)])
    submit = SubmitField("Login")


@app.route("/")
@app.route("/index.html")
def index():
    return render_template("index.html")


@app.route("/aboutus")
@app.route("/aboutus.html")
def aboutus():
    return render_template("aboutus.html")


@app.route("/academics")
@app.route("/academics.html")
def academics():
    return render_template("academics.html")


@app.route("/admission")
@app.route("/admission.html")
def admission():
    return render_template("admission.html")


@app.route("/categories")
def categories():
    return render_template("categories")


@app.route("/register", methods=["GET", "POST"])
def register():
    form = AdmissionForm()

    if form.validate_on_submit():
        name = form.username.data
        email = form.email.data
        password = form.password.data

        try:
            conn = mysql.connect()
            cursor = conn.cursor()
            cursor.execute(
                "INSERT INTO user (name, email, password) VALUES (%s, %s, %s)",
                (name, email, password),
            )
            conn.commit()
            cursor.close()
            conn.close()
            return redirect(url_for("login"))
        except Exception as e:
            return f"Database Error: {e}"

    return render_template("register.html", form=form)


@app.route("/login", methods=["GET", "POST"])
@app.route("/login.html", methods=["GET", "POST"])
def login():
    form = LoginForm()

    if form.validate_on_submit():
        email = form.email.data
        password = form.password.data

        conn = mysql.connect()
        cursor = conn.cursor()
        cursor.execute(
            "SELECT * FROM user WHERE email = %s AND password = %s",
            (email, password),
        )
        user = cursor.fetchone()
        cursor.close()
        conn.close()

        if user:
            return redirect(url_for("dashboard"))
        return "Invalid credentials. Please try again."

    return render_template("login.html", form=form)


@app.route("/dashboard")
@app.route("/dashboard.html")
def dashboard():
    return render_template("dashboard.html")


if __name__ == "__main__":
    app.run(debug=True, port=8000)
