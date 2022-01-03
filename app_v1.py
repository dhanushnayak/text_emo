import streamlit as st
import pandas as pd
import numpy as np
from model_of_text_to_emotion import Text_to_emotion as text_to_emo
import altair as alt
import sys
import time

check = text_to_emo()
st.set_page_config(
     page_title="Text to Emotion",
     page_icon="🧊",
     layout="wide",
     initial_sidebar_state="expanded",
     )
@st.cache(show_spinner=False)
def Get_Prediction(text):
    # do stuff
    val = check.predict(text)
    time.sleep(2)
    return val
def main():
    _, title_col, _ = st.columns([1, 2, 1])

    with title_col:
        st.markdown(
        "<h1>Text to Emotion</h1>", unsafe_allow_html=True
        )
        st.write('')
        my_bar = st.progress(0)
        for i in range(100):time.sleep(0.1); my_bar.progress(i+1)
        st.write('')
        st.subheader("Text says everything")
        st.sidebar.image("https://www.meaningcloud.com/wp-content/uploads/2019/11/Plutchik-wheel.png")    
        st.write('')             
        with st.form(key="emotion_text_form"):
                text = st.text_area("Type Here")
                submit_text = st.form_submit_button(label='Submit')

    if submit_text:
            
            _,col1,col2,_= st.columns([1,1,1,1])
            with st.spinner('Fetching result...'):val=Get_Prediction(text)
            with col1:
                st.write('')
                st.subheader('Emotion  with confidence :')
                a = str(val[0]).capitalize() + " :   " +str(round(val[1]['Confidence'].max()*100,2)) + "  %"
                st.success(a)
                
            with col2:
                st.write('')
                fig= alt.Chart(val[1]).mark_bar().encode(x='Emotions',y='Confidence')
                st.altair_chart(fig,use_container_width=True)
            st.balloons()
        
        
    
if __name__=='__main__':
    main()