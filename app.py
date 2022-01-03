import streamlit as st
import pandas as pd
import numpy as np
import joblib
import altair as alt
pipe_lr = joblib.load(open("Logistic_time_countvector.pkl",'rb'))

def predict_emotion(docx):
    return str(pipe_lr.predict([docx])[0]).capitalize()

def predict_probo(docx):
    return pipe_lr.predict_proba([docx])

def main():
    st.title("Emotion of Text")
    menu = ['Home',"Monitor",'About']
    choice = st.sidebar.selectbox("Menu",menu)
    if choice=="Home":
        #st.subheader("Home")
        with st.form(key="emotion_text_form"):
            raw_text = st.text_area("Type Here")
            submit_text = st.form_submit_button(label='Submit')
        if submit_text:
            col1,col2= st.columns(2)

            predict = predict_emotion(raw_text)
            proba_predict = predict_probo(raw_text)

            with col1:
                st.success("Original Text")
                st.write(raw_text)

                st.success("Prediction")
                st.write(predict)
                st.write("Confidence: {}".format(round(np.max(proba_predict),3)))

            with col2:
                st.success("Prediction Probability")
                proda_df = pd.DataFrame(proba_predict,columns=pipe_lr.classes_)
                proda_clean=proda_df.T.reset_index()
                proda_clean.columns =['Emotions',"Confidence"]
                #st.write(proda_clean)

                fig = alt.Chart(proda_clean).mark_bar().encode(x='Emotions',y='Confidence')
                st.altair_chart(fig,use_container_width=True)

    elif choice=="Monitor":
        st.subheader("Monitor App")
    
    else:
        st.subheader("About me")

if __name__=='__main__':
    main()