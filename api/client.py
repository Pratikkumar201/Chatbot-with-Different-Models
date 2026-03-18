# Mobile App / Web APP
import requests 
import streamlit as st

def get_phi_response(input_text):
    response = requests.post("http://localhost:8000/essay/invoke",
    json = {'input': {'topic': input_text}})

    return response.json()['output']

def get_ollama_response(input_text):
    response = requests.post("http://localhost:8000/poem/invoke",
    json = {'input': {'topic': input_text}})

    return response.json()['output']


st.title("Langchain with LLAMA")
input_text = st.text_input("Write an essay on")
input_text1 = st.text_input("Write a poem on")

if input_text:
    st.write(get_phi_response(input_text))

if input_text1:
    st.write(get_ollama_response(input_text1))
