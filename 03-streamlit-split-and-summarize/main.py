
#streamlit
import streamlit as st
from langchain_groq import ChatGroq
from langchain_core.prompts import PromptTemplate
from dotenv import load_dotenv, find_dotenv
import os
load_dotenv(find_dotenv())

GROQ_API_KEY = os.getenv("GROQ_API_KEY")

#model configuration
model = ChatGroq(
api_key=GROQ_API_KEY,
model="llama3-70b-8192",
)
