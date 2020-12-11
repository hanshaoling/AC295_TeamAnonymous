from flask import Flask,request,Response,send_file
from flask_restful import Resource,Api
import json
import pandas as pd
import numpy as np
import requests
import tensorflow as tf
from Services import get_essay_score
app = Flask(__name__)
api = Api(app)
gap_img_path = 'gap_images/gap_images/'

essay_prompt_dict={"Effect of Computer on people": 1,
                   "Censorship in the libraries" : 2,
                   "Source dependant essay: ROUGH ROAD AHEAD: Do Not Exceed Posted Speed Limit" : 3,
                   "Source dependant essay: Winter Hibiscus by Minfong Ho" : 4,
                   "Source dependant essay: From Home: The Blueprints of Our Lives" : 5,
                   "Source dependant essay: The Mooring Mast" : 6,
                   "Patience" : 7,
                   "The benefits of laughter" : 8}
class EssayScore(Resource):
    def get(self):
        
        return "Please use post method"
    def post(self):
        essay= request.get_json()['essay']
        essay_prompt = request.get_json()['essay_prompt']
        essay_prompt = essay_prompt_dict[essay_prompt]
        score=get_essay_score(essay_prompt,essay)
        return score
            

api.add_resource(EssayScore, '/EssayScore')
    
if __name__=="__main__":
    # determine what the URL for the database should be, port is always 8082 for DB

    app.run(host='0.0.0.0', port=8082, debug=True)


