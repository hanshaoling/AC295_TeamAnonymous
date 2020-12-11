from flask import Flask,render_template,request,make_response,send_file
from flask_restful import Resource,Api
import requests
import io
import json
import os

img_folder = os.path.join('static', 'img')

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = img_folder
api = Api(app)

class GetEssayScore(Resource):
    def get(self):
        headers = {'Content-Type': 'text/html'}
        return make_response(render_template('input.html'),200,headers)
    def post(self):
        essay_text=request.form['essay']
        Bert_filename = os.path.join(app.config['UPLOAD_FOLDER'], 'Bert.jpg')
        essay_prompt=request.form['method']
        db_url = "http://mywebdb:8082/EssayScore"
        #db_url = "http://0.0.0.0:8082/EssayScore"
        resp = requests.post(url=db_url, json={'essay': essay_text, 'essay_prompt': essay_prompt})
        score = float(resp.text)
        if resp.status_code==400:
            return resp.text
        headers = {'Content-Type': 'text/html'}
        return make_response(render_template('result.html', essay=essay_text,user_image=Bert_filename,prompt=essay_prompt,score=score),200,headers)

        if resp.status_code==400:
            return resp.text
        else:
            imagebyte=io.BytesIO(resp.content)
            imagebyte.seek(0)
            return send_file(imagebyte, mimetype='image/jpeg')

class SimilarImage(Resource):
    def get(self):
        headers = {'Content-Type': 'text/html'}
        return make_response(render_template('similar_image.html'),200,headers)
    def post(self):
        image = request.files['image_file']
        method = request.form['method']
        image.save('frontend_upload.jpg')
        url = "http://mywebdb:8082/GetSimilarImage"
        method ={'method':method}
        files = {
            'json': (None, json.dumps(method), 'application/json'),
            'image_file': open('frontend_upload.jpg','rb')
        }
        
        resp = requests.post(url, files=files)
        imagebyte=io.BytesIO(resp.content)
        imagebyte.seek(0)
        return send_file(imagebyte, mimetype='image/jpeg')

api.add_resource(GetEssayScore, '/GetEssayScore')

if __name__=="__main__":
    app.run(host='0.0.0.0', port=8081, debug=True)
    

