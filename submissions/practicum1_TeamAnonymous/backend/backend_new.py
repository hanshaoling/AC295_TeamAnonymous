from flask import Flask,request,Response,send_file
from flask_restful import Resource,Api
from PIL import Image
import json
import dask.dataframe as dd
import dask.array as da
import pandas as pd
import numpy as np
import requests
import tensorflow as tf
from dask.diagnostics import ProgressBar
import glob
from tqdm import tqdm
from tensorflow.keras.models import Model
from tensorflow.keras.models import model_from_json
from Services import resize_flatten_img, cosine_similarity, find_most_similar_img, load_model, prepare_ae_input, get_feature_maps,find_most_similar_img_ae


app = Flask(__name__)
api = Api(app)
gap_img_path = 'gap_images/gap_images/'

class GetSimilarImage(Resource):
    def get(self):
        
        return "Please use post method"
    def post(self):
        image = request.files['image_file']
        method=json.loads(request.form['json'])
        if method['method']=='cosine similarity':
            image = request.files['image_file']
            input_image=Image.open(image)
            output_image = find_most_similar_img(input_image)
            return send_file(output_image, mimetype='image/jpeg')
        else:
            image = request.files['image_file']
            weights = 'ae_weights.h5'; json_file_path = 'autoencoder.json'
            ae = load_model(json_file_path, weights)
            output_image = find_most_similar_img_ae(ae,image)
            return send_file(output_image, mimetype='image/jpeg')
            
class GetImagebyname(Resource):
    def get(self):
        
        return "Please use post method"
    def post(self):
        image_name = request.get_json()['image_name'] 
        artist = request.get_json()['artist'] 
        collection = request.get_json()['collection'] 
        genre = request.get_json()['genre'] 
        df=dd.read_csv("metadata.csv")
        if image_name !='':
            if image_name[-4:]!='.jpg':
                full_image_name=image_name+'.jpg'
            else:
                full_image_name=image_name
            df_select=df[df['original_image_name']==full_image_name]
            image_id=df_select.file_id.compute().values
            if image_id.shape[0]==0:
                return Response(response=f'No such image {image_name} in the database',status=400)
            else:
                image_path= gap_img_path+image_id[0]
                return send_file(image_path, mimetype='image/jpeg')
        elif artist=='' and collection=='' and genre=='':
            return Response(response=f'No information provided',status=400)
        else:
            if artist!='':
                df=df[df['Artist']==artist]
            if collection!='':
                df=df[df['Collection']==collection]
            if genre !='':
                df=df[df['Genre']==genre]
            image_id=df.file_id.compute().values
            if image_id.shape[0]==0:
                return Response(response=f'No such image {image_name} in the database',status=400)
            else:
                image_path= gap_img_path+image_id[0]
                return send_file(image_path, mimetype='image/jpeg')
            

api.add_resource(GetSimilarImage, '/GetSimilarImage')
api.add_resource(GetImagebyname, '/GetImagebyname')
    
if __name__=="__main__":
    # determine what the URL for the database should be, port is always 8082 for DB

    app.run(host='0.0.0.0', port=8082, debug=True)


