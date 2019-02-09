from flask import Flask, render_template,request

app = Flask(__name__)

@app.route('/')
def index():
    return render_template("index.html")

@app.route('/check/', methods = ['GET', 'POST'])
def upload_file():
    if request.method == 'GET':
        return render_template('upload_file.html')
    if request.method == 'POST':
        predicted_flower = 'Lily'
        return render_template('result_file.html', flower = predicted_flower)

if __name__ == "__main__":
    app.run()