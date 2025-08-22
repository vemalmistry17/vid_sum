import streamlit as st
import requests
import os

st.title("Video Summarisation")

uploaded_file = st.file_uploader("Upload a video", type=["mp4"])

if uploaded_file:
    st.video(uploaded_file)
    if st.button("Summarise Video"):
       files = {"file": uploaded_file.getvalue()}
       response = requests.post("http://backend:8000/process/", files=files)
       
       if response.status_code == 200:
           st.success("Video processed successfully!")
           video_bytes = response.content
           st.video(video_bytes)
           
       else:
           st.error("Failed to process video.")