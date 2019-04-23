from flask import Flask, render_template, request
from werkzeug.utils import secure_filename
import requests
import os

app = Flask(__name__)

ALLOWED_EXTENSIONS = set(['jpg', 'jpeg',])
ENGINE_URL = "http://3.212.166.121"

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS   

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/query/<modality>', methods=['GET', 'POST'])
def query(modality):
    if request.method == "POST":
        try:
            query_url = ENGINE_URL + "/query/" + modality
            if "text" == modality:
                query_input = request.form["text"]
                data = {"text": request.form["text"]}
                r = requests.post(query_url, data = data)
            elif "image" == modality:
                query_input = ENGINE_URL + "/uploads/" + f.filename
                if 'file' in request.files:
                    f = request.files['file']
                    if f.filename and allowed_file(f.filename):
                        files = {'file': (f.filename, f)}
                        r = requests.post(query_url, files = files)
            elif "index" == modality:
                query_input = request.args['query_input']
                data = {
                    "index": request.args["index"], 
                    "target": request.args["target"]}
                r = requests.post(query_url, data = data)
            else:
                return "Modality '{}' not supported".format(modality)
            results = r.json()
            return render_template('results.html', 
                modality=modality, 
                input=query_input, 
                results = results, 
                num_datasets = len(results), 
                num_results = 5,
                engine_url = ENGINE_URL)
        except JSONDecodeError as e:
            return str(results)
    elif request.method == "GET":
        return home()
    else:
        return "Method '{}' not supported".format(request.method)

if __name__ == "__main__":
    print("ALLOWED_EXTENSIONS: ", ALLOWED_EXTENSIONS)
    print("ENGINE_URL: ",ENGINE_URL)
    app.run(
        host=os.getenv('LISTEN', '0.0.0.0'),
        port=int(os.getenv('PORT', '81'))
    )
