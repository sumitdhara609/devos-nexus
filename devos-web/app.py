from flask import Flask, render_template, request, redirect, url_for, send_file
from flask_sqlalchemy import SQLAlchemy
from flask_login import (
    LoginManager,
    UserMixin,
    login_user,
    logout_user,
    login_required,
    current_user
)
from datetime import datetime
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import io

app = Flask(__name__)

# =========================
# Security
# =========================
app.config["SECRET_KEY"] = "devos-secret-key"

# =========================
# Database Configuration
# =========================
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///devos.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db = SQLAlchemy(app)

# =========================
# Login Manager
# =========================
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = "login"


# =========================
# Models
# =========================

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), unique=True, nullable=False)
    password = db.Column(db.String(100), nullable=False)


class Session(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    problem = db.Column(db.String(200), nullable=False)
    difficulty = db.Column(db.String(20), nullable=False)
    time_taken = db.Column(db.Integer, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"))

    def __repr__(self):
        return f"<Session {self.problem}>"


# =========================
# User Loader
# =========================

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


# =========================
# Auth Routes
# =========================

@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        username = request.form.get("username", "").strip()
        password = request.form.get("password", "").strip()

        if not username or not password:
            return redirect(url_for("register"))

        existing_user = User.query.filter_by(username=username).first()

        if existing_user:
            return redirect(url_for("login"))

        new_user = User(username=username, password=password)
        db.session.add(new_user)
        db.session.commit()

        return redirect(url_for("login"))

    return render_template("register.html")


@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form.get("username", "").strip()
        password = request.form.get("password", "").strip()

        user = User.query.filter_by(
            username=username,
            password=password
        ).first()

        if user:
            login_user(user)
            return redirect(url_for("home"))

    return render_template("login.html")


@app.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for("login"))


# =========================
# Main Routes
# =========================

@app.route("/")
@login_required
def home():
    sessions = Session.query.filter_by(
        user_id=current_user.id
    ).order_by(Session.created_at.desc()).all()

    total_sessions = len(sessions)
    total_time = sum(session.time_taken for session in sessions)

    avg_time = round(total_time / total_sessions, 1) if total_sessions else 0

    easy = sum(1 for session in sessions if session.difficulty == "Easy")
    medium = sum(1 for session in sessions if session.difficulty == "Medium")
    hard = sum(1 for session in sessions if session.difficulty == "Hard")

    # Performance Score
    a_score = min(total_sessions * 5, 100)

    # Smart Insights
    advice = []

    if total_sessions == 0:
        advice.append("Start logging sessions to unlock analytics.")

    if total_sessions >= 5:
        advice.append("Consistency rising. Keep momentum alive.")

    if avg_time > 35:
        advice.append("Your solving speed can improve with timed practice.")

    if easy > medium + hard:
        advice.append("You dominate Easy mode. Move into Medium challenges.")

    if hard >= 3:
        advice.append("Strong resilience detected. Hard problem exposure is growing.")

    if a_score >= 80:
        advice.append("Elite performance zone reached.")

    return render_template(
        "index.html",
        sessions=sessions,
        total_sessions=total_sessions,
        total_time=total_time,
        avg_time=avg_time,
        easy=easy,
        medium=medium,
        hard=hard,
        a_score=a_score,
        advice=advice,
        owner_name="Sumit Dhara"
    )


@app.route("/add", methods=["POST"])
@login_required
def add():
    problem = request.form.get("problem", "").strip()
    difficulty = request.form.get("difficulty", "").strip()
    time_taken = request.form.get("time_taken", "").strip()

    if not problem or not difficulty or not time_taken.isdigit():
        return redirect(url_for("home"))

    new_session = Session(
        problem=problem,
        difficulty=difficulty,
        time_taken=int(time_taken),
        user_id=current_user.id
    )

    db.session.add(new_session)
    db.session.commit()

    return redirect(url_for("home"))


@app.route("/chart")
@login_required
def chart():
    sessions = Session.query.filter_by(user_id=current_user.id).all()

    easy = sum(1 for s in sessions if s.difficulty == "Easy")
    medium = sum(1 for s in sessions if s.difficulty == "Medium")
    hard = sum(1 for s in sessions if s.difficulty == "Hard")

    labels = ["Easy", "Medium", "Hard"]
    values = [easy, medium, hard]

    plt.style.use("dark_background")

    fig, ax = plt.subplots(figsize=(7, 5))

    bars = ax.bar(labels, values, color="#d4af37")

    ax.set_title("Difficulty Breakdown", fontsize=16, pad=18)
    ax.set_xlabel("Difficulty")
    ax.set_ylabel("Solved Count")

    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)

    for bar in bars:
        height = bar.get_height()
        ax.text(
            bar.get_x() + bar.get_width() / 2,
            height + 0.1,
            str(height),
            ha="center",
            fontsize=11,
            color="white"
        )

    img = io.BytesIO()
    plt.tight_layout()
    plt.savefig(img, format="png", transparent=True)
    img.seek(0)
    plt.close()

    return send_file(img, mimetype="image/png")


# =========================
# Run App
# =========================

if __name__ == "__main__":
    with app.app_context():
        db.create_all()

    app.run(debug=True)