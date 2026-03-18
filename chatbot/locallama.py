from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_community.llms import Ollama
import streamlit as st
import os
from dotenv import load_dotenv

load_dotenv()


prompt = ChatPromptTemplate.from_messages(
    [
        ("system", "You are a helpful assistant. Please response to the user queries."),
        ("user", "Question: {question}")
    ]
)

st.title("Langchain Demo with LLama")
input_text = st.text_input("Search the topic you want")

llm = Ollama(model = "llama3.2:1b")
output_parser = StrOutputParser()
chain = prompt|llm|output_parser   ##(This is the Langchain Expression language, It means user input- prompt template - LLM model- output parser- final response)

if input_text:
    with st.spinner("🤖 Thinking..."):
        st.write(chain.invoke({'question': input_text}))

    # with st.spinner("🤖 Thinking..."):
    # response = chain.invoke({'question': input_text})
    # st.write(response)
    