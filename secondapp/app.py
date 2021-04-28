from flask import Flask, render_template, request, redirect

app = Flask(__name__)

@app.route('/form')
def form():
    return render_template('form.html')

@app.route('/form-submit', methods=['POST'])
def handleFormSubmission():
    if "input-data" in request.form:
        return "successfully received input: " + request.form["input-data"]
    else:
        return "did not receive input"

if __name__ == '__main__':
    app.run(host="0.0.0.0")