from flask import Flask, request, render_template, redirect
from werkzeug.utils import secure_filename
import json,os,subprocess,re,requests
import platform

if platform.platform()[3] == "Win" :
	url_ws = "http://192.168.99.100"
else :
	url_ws = "http://localhost"	


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
        if textarea is not None :
            textarea = request.form['text']
            if textarea != '' :
               url = url_ws + ":5002/txt2pn"
               inpt = json.dumps({'text': textarea})
               head = {'content-type': 'application/json','charset' : 'utf-8'}
               res = requests.post(url, data = inpt,headers = head)
               json_done = res.json()
               return render_template("home.html", Done_2 = json_done)
        elif file is not None :
            text = request.form['file']
            if text != '' :
              url = url_ws + ":5001/pdf2txt"
              files = {'file': open(text, 'rb')}
              res = requests.post(url, files=files)
              json_done = res.json()
              return render_template("home.html", Done_1 = json_done)
        else : 
            return render_template("home.html")
    return render_template("home.html")

if __name__ == "__main__":
    app.run(host='0.0.0.0')