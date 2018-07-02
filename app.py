from flask import Flask, request, render_template, redirect
from werkzeug.utils import secure_filename
import json,os,subprocess,re,requests

UPLOAD_FOLDER = 'uploads/'
TIKA_EXE = 'external/'
TIKA_INPT = 'uploads/temps.pdf'
FULL = os.getcwd()

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['TIKA_EXE'] = TIKA_EXE
app.config["TIKA_INPT"] = TIKA_INPT
app.config["FULL"] = FULL

@app.route('/', methods=['GET', 'POST'])
def contact():
    if request.method == 'POST':
        pattern = request.form.get('pattern', None)
        file = request.form.get('file', None)
        textarea = request.form.get('text',None)
        if pattern is not None and textarea is not None :
            pattern2 = request.form['pattern']
            textarea2 = request.form['text']
            result = str(len(re.findall(pattern2,textarea2)))
            result = { 'pattern' : pattern2 , 'nb_occur' : result}
            return render_template("home.html", Done_2 = result)
        elif file is not None :
            text = request.form['file']
            if text != '' :
              url = "http://192.168.99.100:5001/pdf2txt"
              files = {'file': open(text, 'rb')}
              res = requests.post(url, files=files)
              json_done = res.json()
              return render_template("home.html", Done_1 = json_done)
        else : 
            return render_template("home.html")
    return render_template("home.html")

if __name__ == "__main__":
    app.run(host='0.0.0.0')