import joblib
from neattext import TextExtractor
from tensorflow.keras.models import model_from_json
from tensorflow.keras.preprocessing.sequence import pad_sequences
import pandas as pd
import tensorflow
token_loaded = joblib.load("model/tokenizer_text_emotion.pickle")
onehot_loaded = joblib.load("model/onehot_encoder_text_emotion.pkl")
json_file = open('model/Keras_model_for_text_emotion.json', 'r')
loaded_model_json = json_file.read()
json_file.close()
model = model_from_json(loaded_model_json)
model.load_weights("model/Keras_model_for_text_emotion_weights.h5")

class Text_to_emotion():
    def __init__(self):
        '''
        model base path is provided to load needed model
        
        '''
        
    
    def preprocess(self,text):
        '''
        input : text
        output : removed username, stopwords and puncts for text
        used neattext to remove the data
        
        '''
        sentx1 = TextExtractor(text=text)
        text1=sentx1.remove_puncts().remove_stopwords().remove_userhandles().text
        return text1
    
    def predict(self,text):
        '''
        Input : text
        Output : Emotion and confidence of each emotion as dataframe
        
        '''
        text = self.preprocess(text)
        intok=token_loaded.texts_to_sequences([text])
        seqin = pad_sequences(intok, padding='pre',maxlen=256) # padding the sequence with length 256
        a= model.predict([seqin]) # predict model output
        b = model.predict_proba([seqin]) # predict confidence
        df=pd.DataFrame({"Emotions":onehot_loaded.categories_[0],"Confidence":b[0]})
        return onehot_loaded.inverse_transform(a)[0][0],df