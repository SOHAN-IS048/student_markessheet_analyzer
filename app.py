from flask import Flask, render_template, request
import psycopg2
import os

app = Flask(__name__)

# ✅ Get the DATABASE_URL from environment variable
DATABASE_URL = os.environ.get("DATABASE_URL")

# ✅ Initialize PostgreSQL DB
def init_db():
    conn = psycopg2.connect(DATABASE_URL)
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS students (
            id SERIAL PRIMARY KEY,
            name TEXT,
            marks REAL,
            result TEXT
        )
    """)
    conn.commit()
    conn.close()

init_db()

@app.route("/", methods=["GET", "POST"])
def index():
    students = []
    average = 0
    topper = {"name": "", "marks": 0}
    pass_count = 0
    fail_count = 0

    if request.method == "POST":
        conn = psycopg2.connect(DATABASE_URL)
        cursor = conn.cursor()

        for i in range(1, 4):
            name = request.form.get(f"name{i}")
            marks = float(request.form.get(f"marks{i}"))
            result = "Pass" if marks >= 35 else "Fail"

            students.append({"name": name, "marks": marks, "result": result})

            # ✅ Insert into PostgreSQL
            cursor.execute(
                "INSERT INTO students (name, marks, result) VALUES (%s, %s, %s)",
                (name, marks, result)
            )

            if result == "Pass":
                pass_count += 1
            else:
                fail_count += 1

        conn.commit()
        conn.close()

        average = round(sum(s['marks'] for s in students) / len(students), 2)
        topper = max(students, key=lambda s: s["marks"])

    return render_template("index.html",
                           students=students,
                           average=average,
                           topper=topper,
                           pass_count=pass_count,
                           fail_count=fail_count)

if __name__ == "__main__":
    app.run(debug=True)
