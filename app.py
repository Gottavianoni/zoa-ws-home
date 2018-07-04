from flask import Flask, request, render_template, redirect
from werkzeug.utils import secure_filename
import json,os,subprocess,re,requests
import platform
import socket

try :
    uni = str(requests.get("http://" + socket.gethostname() + ":5001/pdf2txt" ).status_code)
except :
    uni = "FAIL"	
try :
    win = str(requests.get("http://192.168.99.100:5001/pdf2txt").status_code)
except :
    win = "FAIL"


if win == "200" :
  url_ws = "http://192.168.99.100"
else :
  url_ws = "http://" + socket.gethostname()

UPLOAD_FOLDER = 'temp/'
FULL = os.getcwd()

app = Flask(__name__)

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config["FULL"] = FULL

@app.route('/', methods=['GET', 'POST'])
def contact():
    if request.method == 'POST':
        pattern = request.form.get('pattern', None)
        try : 
          file = request.files['file']
        except :
          pass
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
        elif file.filename != '':
              url = url_ws + ":5001/pdf2txt"
              filename = secure_filename(file.filename)
              filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
              filepath_ascii = filepath.encode("ascii","ignore")
              try :
                file.save(filepath)
              except :
                file.save(filepath_ascii)
                filepath = filepath_ascii
              file_op = open(filepath, 'rb')
              files = {'file': file_op }
              res = requests.post(url, files=files)
              json_done = res.json()
              file_op.close()
              os.remove(filepath)
              return render_template("home.html", Done_1 = json_done)
        else : 
            return render_template("home.html")
    return render_template("home.html")

if __name__ == "__main__":
    app.run(host='0.0.0.0')