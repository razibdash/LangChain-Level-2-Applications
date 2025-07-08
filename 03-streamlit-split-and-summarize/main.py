
#streamlit
import streamlit as st
from langchain_groq import ChatGroq
from langchain_core.prompts import PromptTemplate
from dotenv import load_dotenv, find_dotenv
from langchain.chains.summarize import load_summarize_chain
from langchain.text_splitter import RecursiveCharacterTextSplitter
import pandas as pd
from io import StringIO
import os
load_dotenv(find_dotenv())

GROQ_API_KEY = os.getenv("GROQ_API_KEY")

#model configuration
model = ChatGroq(
api_key=GROQ_API_KEY,
model="llama3-70b-8192",
)

#Page title and header
st.set_page_config(page_title="AI Long Text Summarizer")
st.header("AI Long Text Summarizer")

st.markdown("ChatGPT cannot summarize long texts. Now you can do it with this app.")


# Input
st.markdown("## Upload the text file you want to summarize")

uploaded_file = st.file_uploader("Choose a file", type="txt")

# Output
st.markdown("### Here is your Summary:")
if uploaded_file is not None:
    bytes_data = uploaded_file.getvalue()
    # Read the file content
    # To convert to a string based IO:
    stringio = StringIO(uploaded_file.getvalue().decode("utf-8"))
    # To read file as string:
    string_data = stringio.read()
    
    file_input = string_data
    
    if len(file_input.split(" ")) > 20000:
        st.write("Please enter a shorter file. The maximum length is 20000 words.")
        st.stop()

    text_splitter = RecursiveCharacterTextSplitter(
        separators=["\n\n", "\n"], 
        chunk_size=5000, 
        chunk_overlap=350
        )
    # Split the text into manageable chunks
    splitted_documents = text_splitter.create_documents([file_input])
    
    # Define the prompt template for summarization
    template = """
    You are an AI assistant that summarizes long texts. 
    Please summarize the following text in a concise manner:
    
    TEXT: {text}
    
    SUMMARY:
    """
    
    # Create a prompt template with the input variables and the template
    prompt = PromptTemplate(
        input_variables=["text"],
        template=template,
    )
    
    # Generate the summary using the model and prompt
    response = model.invoke(prompt.format(text=splitted_documents[0].page_content))
    
    # Display the generated summary
    st.write(response.content)