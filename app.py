from flask import Flask, render_template, request
import pandas as pd
import os

app = Flask(__name__)

@app.route("/", methods=["GET", "POST"])
def index():
    students = []
    average = 0
    topper = {"name": "", "marks": 0}
    pass_count = 0
    fail_count = 0

    if request.method == "POST":
        for i in range(1, 4):
            name = request.form.get(f"name{i}")
            marks = float(request.form.get(f"marks{i}"))
            result = "Pass" if marks >= 35 else "Fail"

            students.append({
                "name": name,
                "marks": marks,
                "result": result
            })

            if result == "Pass":
                pass_count += 1
            else:
                fail_count += 1

        average = round(sum(s['marks'] for s in students) / len(students), 2)
        topper = max(students, key=lambda s: s["marks"])

        # ✅ Save to CSV
        df = pd.DataFrame(students)
        file_path = "student_data.csv"
        write_header = not os.path.exists(file_path)
        df.to_csv(file_path, mode='a', header=write_header, index=False)

    return render_template("index.html",
                           students=students,
                           average=average,
                           topper=topper,
                           pass_count=pass_count,
                           fail_count=fail_count)

if __name__ == "__main__":
    app.run(debug=True)
