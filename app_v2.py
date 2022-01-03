#from mongo_data import Mongo_data
import streamlit as st
import pandas as pd
import time

# Security
#passlib,hashlib,bcrypt,scrypt

# DB Management

import numpy as np
from model_of_text_to_emotion import Text_to_emotion as text_to_emo
from mongo_data import Mongo_data
import altair as alt
import sys
import time

mon = Mongo_data()
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


def main_1():
		val=[0,0]
		text=0
		sid_col, title_col, _ = st.columns([1, 2, 1])
		with title_col:
		
			st.write('')
			my_bar = st.progress(0)
			for i in range(100):time.sleep(0.1); my_bar.progress(i+1)
			st.write('')
			st.subheader("Text says everything")
			
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
		return val[0],text
class my_emotion():
	def __init__(self):
		st.title("Text to Emotion App")
		menu = ["Home","Login","SignUp"]
		st.sidebar.image("https://www.meaningcloud.com/wp-content/uploads/2019/11/Plutchik-wheel.png")    
		self.choice = st.sidebar.selectbox("Menu",menu)
		self.login = 0 
		self.user = 0
		
	def create_user(self):
		st.subheader("Create New Account")
		new_user = st.text_input("Email",help='*****@gmail.com')
		new_password = st.text_input("Password",type='password')

		if st.button("Signup"):
			if str(new_user).endswith('@gmail.com'):
				mon.insert_user(username=new_user,password=new_password)
				#add_userdata(new_user,new_password)

				st.success("You have successfully created a valid Account")
				st.info("Go to Login Menu to login")
				
			else:
				st.error("Please provide email")

	def loginpage(self):
		username = st.sidebar.text_input("Email")
		password = st.sidebar.text_input("Password",type='password')
		if st.sidebar.checkbox("Login"):
			# if password == '12345':
			
		
			kls = mon.push_org_login(user=username,password=password)
			result =mon.get_login(user=username,password=password)
			if result==1:
				self.login=1
				st.success("Logged In as {}".format(username))
				self.user = username

			elif result==0:
				st.warning("Account not exist")
				st.info("Please go to sign up section")
			else:
				st.warning("Incorrect Username/Password ")
			

	def home(self,status=0,func=None):
		if status==0:
			st.write("")
			con = st.container()
			with con:
				st.write("")
				st.image("https://www.certifiedfinancialguardian.com/images/blog-wp-login.png")
				_,please,_1 = st.columns([1,2,1])
				with _:
					st.info("⬅")
				with please:
					st.info("Please Login")
				with _1:
					st.info("The App is locked")
		if status==1:
			func
	def text_page(self):
		con,te=main_1()
		mon.text_feed(emotion=con,text=te,user=self.user)
def main():
	my_emo = my_emotion()
	if my_emo.choice=='SignUp': my_emo.create_user()
	if my_emo.choice=='Home': my_emo.home()
	if my_emo.choice=='Login': my_emo.loginpage()
	if my_emo.login==1: my_emo.text_page()


	
if __name__ == '__main__':
	main()