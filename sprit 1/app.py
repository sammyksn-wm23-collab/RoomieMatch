import os
import sqlite3
from flask import Flask, g, redirect, render_template, request, url_for, flash

app = Flask(__name__)
app.config["DATABASE"] = os.path.join(app.root_path, "campuses.db")
app.secret_key = "dev-secret-key"


def get_db():
    if "db" not in g:
        conn = sqlite3.connect(app.config["DATABASE"])
        conn.row_factory = sqlite3.Row
        g.db = conn
    return g.db


@app.teardown_appcontext
def close_db(_error):
    db = g.pop("db", None)
    if db is not None:
        db.close()


def init_db():
    conn = get_db()
    conn.execute(
        """
        CREATE TABLE IF NOT EXISTS university_campuses (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL UNIQUE,
            city TEXT NOT NULL,
            country TEXT NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
        """
    )
    conn.commit()

    count = conn.execute("SELECT COUNT(*) AS count FROM university_campuses").fetchone()["count"]
    if count == 0:
        conn.executemany(
            "INSERT INTO university_campuses (name, city, country) VALUES (?, ?, ?)",
            [
                ("Main Campus", "Lagos", "Nigeria"),
                ("North Campus", "Abuja", "Nigeria"),
            ],
        )
        conn.commit()


with app.app_context():
    init_db()


@app.route("/")
def index():
    return redirect(url_for("admin_campuses"))


@app.route("/admin/campuses", methods=["GET"])
def admin_campuses():
    campuses = get_db().execute(
        "SELECT id, name, city, country, created_at FROM university_campuses ORDER BY name"
    ).fetchall()
    return render_template("admin_campuses.html", campuses=campuses)


@app.route("/admin/campuses/add", methods=["POST"])
def add_campus():
    name = request.form.get("name", "").strip()
    city = request.form.get("city", "").strip()
    country = request.form.get("country", "").strip()

    if not name or not city or not country:
        flash("Please provide a campus name, city, and country.", "error")
        return redirect(url_for("admin_campuses"))

    try:
        get_db().execute(
            "INSERT INTO university_campuses (name, city, country) VALUES (?, ?, ?)",
            (name, city, country),
        )
        get_db().commit()
    except sqlite3.IntegrityError:
        flash("A campus with that name already exists.", "error")
    else:
        flash(f"Campus '{name}' added successfully.", "success")

    return redirect(url_for("admin_campuses"))


@app.route("/admin/campuses/delete/<int:campus_id>", methods=["POST"])
def delete_campus(campus_id):
    db = get_db()
    campus = db.execute(
        "SELECT name FROM university_campuses WHERE id = ?",
        (campus_id,),
    ).fetchone()

    if campus is None:
        flash("Campus was not found.", "error")
        return redirect(url_for("admin_campuses"))

    db.execute("DELETE FROM university_campuses WHERE id = ?", (campus_id,))
    db.commit()
    flash(f"Campus '{campus['name']}' deleted successfully.", "success")
    return redirect(url_for("admin_campuses"))


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5000)
