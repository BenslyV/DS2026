import streamlit as st

st.title("My First App")
st.write("Hello Bensly 👋")

st.title("Title")
st.header("Header")
st.subheader("Subheader")
st.text("Simple text")
st.write("Smart display")

name = st.text_input("Enter your name")
age = st.slider("Select age", 1, 100)

st.write(name, age)


import pandas as pd

df = pd.DataFrame({
    "Name": ["A", "B"],
    "Age": [25, 30]
})

st.dataframe(df)

import numpy as np

data = np.random.randn(50, 2)
st.line_chart(data)

st.sidebar.title("Menu")
option = st.sidebar.selectbox("Choose", ["Home", "About"])

if st.button("Click Me"):
    st.write("Button clicked!")

with st.form("my_form"):
    name = st.text_input("Name")
    submit = st.form_submit_button("Submit")

if submit:
    st.write(name)

import pickle

model = pickle.load(open("model.pkl", "rb"))

input_val = st.number_input("Enter value")

if st.button("Predict"):
    result = model.predict([[input_val]])
    st.write(result)