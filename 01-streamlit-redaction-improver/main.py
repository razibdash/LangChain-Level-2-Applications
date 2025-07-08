
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

# Define the prompt template for redaction and tone conversion

template = """
Below is a draft text that may be poorly worded.
Your goal is to: - Properly redact the draft text - Convert the draft text to a specified tone - Convert the draft text to a specified dialect

    Here are some examples different Tones:
    - Formal: Greetings! OpenAI has announced that Sam Altman is rejoining the company as its Chief Executive Officer. After a period of five days of conversations, discussions, and deliberations, the decision to bring back Altman, who had been previously dismissed, has been made. We are delighted to welcome Sam back to OpenAI.
    - Informal: Hey everyone, it's been a wild week! We've got some exciting news to share - Sam Altman is back at OpenAI, taking up the role of chief executive. After a bunch of intense talks, debates, and convincing, Altman is making his triumphant return to the AI startup he co-founded.

    Here are some examples of words in different dialects:
    - American: French Fries, cotton candy, apartment, garbage, \
        cookie, green thumb, parking lot, pants, windshield
    - British: chips, candyfloss, flag, rubbish, biscuit, green fingers, \
        car park, trousers, windscreen

    Example Sentences from each dialect:
    - American: Greetings! OpenAI has announced that Sam Altman is rejoining the company as its Chief Executive Officer. After a period of five days of conversations, discussions, and deliberations, the decision to bring back Altman, who had been previously dismissed, has been made. We are delighted to welcome Sam back to OpenAI.
    - British: On Wednesday, OpenAI, the esteemed artificial intelligence start-up, announced that Sam Altman would be returning as its Chief Executive Officer. This decisive move follows five days of deliberation, discourse and persuasion, after Altman's abrupt departure from the company which he had co-established.

    Please start the redaction with a warm introduction. Add the introduction \
        if you need to.

    Below is the draft text, tone, and dialect:
    DRAFT: {draft}
    TONE: {tone}
    DIALECT: {dialect}

    YOUR {dialect} RESPONSE:

"""

# Create a prompt template with the input variables and the template

prompt = PromptTemplate(
input_variables=["draft", "tone", "dialect"],
template=template,
)

#Page title and header
st.set_page_config(page_title="Re-write your text")
st.header("Re-write your text")

#header description
st.markdown("Re-write your text in different styles.")
# Input text area for the draft
st.markdown("## Enter the text you want to re-write")

draft_text = st.text_area(label="Text",  height=200, placeholder="Enter your text here...")

#stop if the draft length is more than 700 words
if len(draft_text.split(" ")) > 700:
    st.write("Please enter a shorter text. The maximum length is 700 words.")
    st.stop()

# Prompt template tunning options

col1, col2 = st.columns(2)
with col1:
    option_tone = st.selectbox(
    'Which tone would you like your redaction to have?',
    ('Formal', 'Informal'))

with col2:
    option_dialect = st.selectbox(
    'Which English Dialect would you like?',
    ('American', 'British'))

# Output

st.markdown("### Your Re-written text:")

prompt_with_draft = prompt.format(
tone=option_tone,
dialect=option_dialect,
draft=draft_text
)

# Generate the response using the model
response = model.invoke(prompt_with_draft)
# Display the response
#streming response
st.write(response.content)