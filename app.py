from flask import Flask, render_template_string, request
import pandas as pd  # ✅ Import pandas

app = Flask(__name__)

# Load HTML and CSS from files
with open("index.html", "r") as f:
    html_template = f.read()

with open("style.css", "r") as f:
    style_css = f"<style>{f.read()}</style>"

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

        # ✅ Calculate average and topper
        average = round(sum(s['marks'] for s in students) / len(students), 2)
        topper = max(students, key=lambda s: s["marks"])

        # ✅ Save to CSV using Pandas
        df = pd.DataFrame(students)
        df.to_csv("student_data.csv", mode='a', header=not pd.io.common.file_exists("student_data.csv"), index=False)

    return render_template_string(style_css + html_template,
                                  students=students,
                                  average=average,
                                  topper=topper,
                                  pass_count=pass_count,
                                  fail_count=fail_count)

if __name__ == "__main__":
    app.run(debug=True)
