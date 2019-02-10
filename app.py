from flask import Flask, render_template,request
from inference import get_flower_name
from commons import get_tensor
app = Flask(__name__)

@app.route('/')
def index():
    return render_template("index.html")

@app.route('/check/', methods = ['GET', 'POST'])
def upload_file():
    if request.method == 'GET':
        return render_template('upload_file.html')
    if request.method == 'POST':
        if "file" not in request.files:
            print("File not uploaded.")
            return
        file = request.files['file']
        image = file.read()
        tensor = get_tensor(image_bytes=image)
        category, flower = get_flower_name(image_bytes=image)
        print(get_tensor(image_bytes=image))
        return render_template('result_file.html', flower = flower)


if __name__ == "__main__":
    app.run()