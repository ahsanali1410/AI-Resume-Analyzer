from flask import Flask, render_template, request
import PyPDF2
import os

app = Flask(__name__)

UPLOAD_FOLDER = "uploads"
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

skills = [
    "python", "java", "c++", "machine learning",
    "html", "css", "javascript", "sql", "flask"
]

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/analyze", methods=["POST"])
def analyze_resume():
    file = request.files["resume"]

    filepath = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
    file.save(filepath)

    text = ""

    with open(filepath, "rb") as pdf_file:
        reader = PyPDF2.PdfReader(pdf_file)

        for page in reader.pages:
            text += page.extract_text()

    text = text.lower()

    found_skills = []

    for skill in skills:
        if skill in text:
            found_skills.append(skill)

    ats_score = len(found_skills) * 10

    return render_template(
        "index.html",
        skills=found_skills,
        score=ats_score
    )

if __name__ == "__main__":
    app.run(debug=True)