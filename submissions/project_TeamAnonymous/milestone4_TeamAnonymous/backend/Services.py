import tensorflow as tf
import json
import numpy as np
from tensorflow import keras
from tensorflow.keras.models import Model,Sequential
from tensorflow.keras.models import model_from_json
from tensorflow.keras.layers.experimental.preprocessing import TextVectorization
from tensorflow.keras.layers import LSTM, Embedding, Dense, GRU, Input
from tensorflow.keras import layers


def build_bert_model():
   '''

   :return: Bert model structure
   '''
   max_len = 512
   input_ids = layers.Input(shape=(max_len,), dtype=tf.int32, name = 'input_ids')
   token_type_ids = layers.Input(shape=(max_len,), dtype=tf.int32, name = 'token_type_ids')
   attention_mask = layers.Input(shape=(max_len,), dtype=tf.int32, name = 'attention_mask')
   encoder = TFBertModel.from_pretrained("bert-base-uncased")
   encoder.trainable=False
   embedding = encoder(
       input_ids, token_type_ids=token_type_ids, attention_mask=attention_mask
   )[1]
   embedding_flatten = layers.Flatten(name="embedding_flatten")(embedding)
   text_dropout=layers.Dropout(0.2)(embedding_flatten)
   bert_dense = layers.Dense(256, name="bert_dense", activation = 'relu')(text_dropout)
   intermediate_dense = layers.Dense(32, name = "intermediate_dense", activation = 'relu')(bert_dense)
   output = layers.Dense(1, activation = 'sigmoid')(intermediate_dense)

   inputs = {'input_ids': input_ids, 'token_type_ids': token_type_ids, 'attention_mask': attention_mask}
   bert_model = keras.Model(inputs= inputs, outputs= output,name='BERT_Model')
   return bert_model
def build_model(model_path='glo_gru'):
    model=tf.keras.models.load_model('glo_gru')
    return model

def get_essay_score(essay_prompt, essay):
    # essay: a string
    # essay_prompt: int
    model=build_model()
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
