from flask import Flask,request,Response,send_file
from flask_restful import Resource,Api
import json
import pandas as pd
import numpy as np
import requests
import tensorflow as tf
app = Flask(__name__)
api = Api(app)

essay_prompt_dict={"Effect of Computer on people": 1,
                   "Censorship in the libraries" : 2,
                   "Source dependant essay: ROUGH ROAD AHEAD: Do Not Exceed Posted Speed Limit" : 3,
                   "Source dependant essay: Winter Hibiscus by Minfong Ho" : 4,
                   "Source dependant essay: From Home: The Blueprints of Our Lives" : 5,
                   "Source dependant essay: The Mooring Mast" : 6,
                   "Patience" : 7,
                   "The benefits of laughter" : 8}

model = tf.keras.models.load_model('glo_gru')
def get_essay_score(essay_prompt, essay,model=model):
    # essay: a string
    # essay_prompt: int
    #load bert weight
    #model.load_weights("BERT_Model.h5")
    '''
    #### missing tokenizer
    tokenizer = BertTokenizer.from_pretrained('bert-base-uncased',do_lower_case=True)
    input_x = tokenizer.encode_plus(essay,
        add_special_tokens = True, # add [CLS], [SEP]
        max_length = 512, # max length of the text that can go to BERT (<=512)
        padding='max_length',
        return_attention_mask = True, # add attention mask to not focus on pad tokens
        truncation='longest_first',
        return_tensors="tf"
    )
    '''
    #print(input_x)

    score = model.predict([essay])[0][0]
    #input_x= tokenizer(...)
    #score=model.predict(input_x))
    low_scale={1:2,2:1,3:0,4:0,5:0,6:0,7:0,8:0}
    high_scale={1:12,2:6,3:3,4:3,5:4,6:4,7:30,8:60}
    score=score*(high_scale[essay_prompt]-low_scale[essay_prompt])+low_scale[essay_prompt]
    score=int(score.round(0))
    return score

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


