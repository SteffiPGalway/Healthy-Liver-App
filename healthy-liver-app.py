import streamlit as st
import base64
import sklearn
import numpy as np
import pickle as pkl
from sklearn.preprocessing import StandardScaler

scal=StandardScaler()

#Reads the pickled version of the object from the open file object
model=pkl.load(open("final_model.p","rb"))

st.set_page_config(
    page_title="Learn to predict the risk of getting fatty liver disease!",
    page_icon="🏥",
    layout="centered",
    initial_sidebar_state="expanded",
    menu_items={
        'About': "This is an app to predict your risk of getting non-alcohol fatty liver disease!"
    })

def preprocess(age,male,weight,height,bmi,futime):  
    # Pre-processing user input   
    if male=="male":
        male=1 
    else: 
        male=0  
    user_input=[age,male,weight,height,bmi,futime]
    user_input=np.array(user_input)
    user_input=user_input.reshape(1,-1)
    user_input=scal.fit_transform(user_input)
    prediction = model.predict(user_input)

    return prediction

# front end elements of the web page 
html_temp = """ 
    <div> 
    <h1 style ="color:black;text-align:center;">Healthy Liver App</h1> 
    </div> 
    """
      
st.markdown(html_temp, unsafe_allow_html = True) 

age=st.selectbox ("Age",range(1,100,1))
male = st.radio("Select sex: ", ('male', 'female'))
weight=st.selectbox('Weight in kg',range(1,300,1))
height=st.selectbox('Height in cm',range(1,200,1))
bmi=st.selectbox('BMI',range(1,50,1))
futime=st.selectbox ("Time to death or last follow up",range(1,10000,1))

pred=preprocess(age,male,weight,height,bmi,futime)

if st.button("Predict"):    
    if pred[0] == 1:
        st.error('Warning! You have high risk of dying from fatty liver!')
    else:
        st.success('You have lower risk of dying from fatty liver!')
        
st.sidebar.subheader("About App")

st.sidebar.info("This web app is helps you to find out whether you are at a risk of dying from fatty liver.")
st.sidebar.info("Enter the required fields and click on the 'Predict' button to check whether you have a healthy liver")
st.sidebar.info("Don't forget to rate this app")

feedback = st.sidebar.slider('How much would you rate this app?',min_value=0,max_value=5,step=1)

if feedback:
    st.header("Thank you for rating the app!")

st.info("Caution: This is just a prediction and not doctoral advice. Kindly see a doctor if you feel the symptoms persist.") 
