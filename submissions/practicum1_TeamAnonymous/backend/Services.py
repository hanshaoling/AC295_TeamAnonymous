from flask import Flask,render_template,request,make_response,send_file
from flask_restful import Resource,Api
import requests
import io
from PIL import Image
import glob
from tensorflow.keras.models import Model
from tensorflow.keras.models import model_from_json
import tensorflow as tf
from tqdm import tqdm
import numpy as np
import dask.array as da
import json

img_shape = (32,32)
gap_img_path = 'gap_images/gap_images/'
def resize_flatten_img(img):
    new_image = img.convert("RGB").resize(img_shape)
    img_array = np.asarray(new_image).reshape(-1,)
    return img_array

def cosine_similarity(img_a, img_b):
    img_a = resize_flatten_img(img_a).astype('float64')/255.; img_b = resize_flatten_img(img_b).astype('float64')/255.
    cos_sim = da.dot(img_a, img_b) / (da.linalg.norm(img_a) * da.linalg.norm(img_b))
    return cos_sim.compute()

def find_most_similar_img(input_img):
    max_sim = -np.inf
    img_list = glob.glob(gap_img_path + '*.jpg')
    for img_b_path in tqdm(img_list):
        img_b = Image.open(img_b_path)
        sim = cosine_similarity(input_img, img_b)
        if sim > max_sim and sim < 0.99999:
            max_sim = sim
            output_img = img_b_path
    return output_img

def load_model(json_file_path,weights):
    json_file = open(json_file_path, 'r')
    loaded_model_json = json_file.read()
    json_file.close()
    ae = model_from_json(loaded_model_json)
    # load weights into new model
    ae.load_weights(weights)
    return ae

#resize image into input size of autoencoder
def prepare_ae_input(filename, resize_dim = (64,64)): 
    im = Image.open(filename).convert('RGB') 
    im = np.array(im)
    resize_im = tf.cast(im, tf.float32)/255.
    resize_im = tf.image.resize(resize_im, resize_dim)
    resize_im = np.expand_dims(resize_im, axis=0)
    return resize_im

#get latent space
def get_feature_maps(model, input_image, layer_id = 7):
    model_ = Model(inputs=[model.input], outputs=[model.layers[layer_id].output])
    return model_.predict(input_image)[0]

def find_most_similar_img_ae(ae, input_img_path):
    img = prepare_ae_input(input_img_path)
    img_ae = get_feature_maps(ae, img)
    img_list = glob.glob(gap_img_path + '*.jpg')
    max_sim = -np.inf
    with open('feature_map.json') as infile:
        feature_map = json.load(infile)
    for img_b_path in tqdm(img_list):
        img_b_ae = np.array(feature_map[img_b_path])
        sim = da.dot(img_ae, img_b_ae) / (da.linalg.norm(img_ae) * da.linalg.norm(img_b_ae))
        sim = sim.compute()
        if sim > max_sim and sim < 0.99999:
            max_sim = sim
            output_img = img_b_path
    return output_img

# gap_img_path = 'gap_images/gap_images/'
# img_shape = (32,32)
# img_list = glob.glob(gap_img_path + '*.jpg')
# feature_map = {}
# weights = 'ae_weights.h5'; json_file_path = 'autoencoder.json'
# ae = load_model(json_file_path, weights)
# for img in tqdm(img_list):
#     img_ae = prepare_ae_input(img)
#     img_feature = get_feature_maps(ae, img_ae)
#     feature_map[img] = img_feature.tolist()

# with open('feature_map.json', 'w') as fp:
#     json.dump(feature_map, fp)
# print("Dump complete")s