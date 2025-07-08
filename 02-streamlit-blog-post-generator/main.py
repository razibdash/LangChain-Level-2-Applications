
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


st.set_page_config(
    page_title = "Blog Post Generator"
)

st.title("Blog Post Generator")

# Define the prompt template for blog post generation
template = """You are a professional blog post writer. Your task is to generate a well-structured and engaging blog post based on the provided {topic}. The blog post should be informative, engaging, and suitable for a general audience.

Title: {topic}

Your blog post:
"""
# Create a prompt template with the input variables and the template
prompt = PromptTemplate(
    input_variables=["topic"],
    template=template,
)

# Input field for the blog post topic
topic = st.text_area(label="Enter the topic",  height=50, placeholder="e.g., 'The Future of AI in Healthcare'")
# Button to generate the blog post
if st.button("Generate Blog Post"):
    if topic:
        # Generate the blog post using the model and prompt
        response = model.invoke(prompt.format(topic=topic))
        # Display the generated blog post
        st.subheader("Generated Blog Post: ")
        st.write(response.content)
    else:
        st.error("Please enter a topic for the blog post.")