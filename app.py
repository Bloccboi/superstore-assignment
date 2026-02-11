import streamlit as st
import pandas as pd
import numpy as np



st.title("Hello,Streamlit!")
st.write("Welcome to your first streamlit app.")


name = st.text_input("Enter your  name:")
st.write(f"Hello,{name}")
checkbox = st.checkbox("Show greeting")
radio = st.radio("Choose a greeting style:", ("formal","Casual"))
date = st.date_input("select a date")
color = st.color_picker("Pick a color:", "#00f900")
image = st.file_uploader("Upload an image:", type = ["png", "jpg","jpeg"])
select = st.select_slider("select", ("Formal","Casual","Native"))
image = st.image("/Users/apple/Documents/Screenshot 2026-01-17 at 08.00.04.png")
video = st.video("/Users/apple/Downloads/Telegram Lite/Power.Book.IV.Force.S03E10.720p.10bit.WEBRip.2CH.x265.HEVC-P.mkv")
audio = st.audio("https://www.youtube.com/watch?v=4IuUYpS9RjE&list=RD4IuUYpS9RjE&start_radio=1&pp=ygULYXNha2UgYXVkaW-gBwE%3D")
st.sidebar.title("Side Menu")
st.sidebar._text_input("Enter your name")
st.sidebar.write(f"MY name is {name}")

first,second = st.columns(2)

with first:
    name = st.text_area("What is your name?")
    st.write(name)

with second:
    audio = st.audio_input("audio")
    chat =st.chat_input("Enter your name")
    if chat:
        st.write(chat)

st.write("Here's our first attempt at using data to create a table:")
st.write(pd.DataFrame({
    'first column': [1, 2, 3, 4],
    'second column': [10, 20, 30, 40]
}))

dataframe = np.random.randn(10, 20)
st.dataframe(dataframe)

chart_data = pd.DataFrame(
     np.random.randn(20, 3),
     columns=['a', 'b', 'c'])

st.line_chart(chart_data)