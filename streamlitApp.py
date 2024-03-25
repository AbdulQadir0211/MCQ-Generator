import os
import json
import traceback
import pandas as pd
from dotenv import load_dotenv
from src.mcqgenerator.utils import read_file, get_table_data
import streamlit as st

from src.mcqgenerator.logger import logging

# load json file
with open('I:\MCQ Generator\Response.json', 'r') as file:
    RESPONSE_JSON = json.load(file)

st.title("MCQ Generator with Gemma and Langchain")

# create a form using st.form
with st.form('user_inputs'):
    # File upload
    upload_file = st.file_uploader("Upload a PDF or txt file")

    # Input fields
    mcq_count = st.number_input("No. of MCQs", min_value=3, max_value=50)
    subject = st.text_input("Insert Subject", max_chars=20)
    tone = st.text_input("Complexity level of Questions", max_chars=20, placeholder="Simple")
    button = st.form_submit_button("Generate MCQs")

    # check if the button is clicked and all fields have input
    if button and upload_file is not None and mcq_count and subject and tone:
        with st.spinner("loading..."):
            try:
                text = read_file(upload_file)
                # Call your MCQ generation function directly
                response = generate_mcqs(text, mcq_count, subject, tone, RESPONSE_JSON)

            except Exception as e:
                traceback.print_exception(type(e), e, e.__traceback__)
                st.error("Error")

            else:
                if isinstance(response, dict):
                    # Extract the quiz data from the response
                    quiz = response.get("quiz", None)
                    if quiz is not None:
                        table_data = get_table_data(quiz)
                        if table_data is not None:
                            df = pd.DataFrame(table_data)
                            df.index = df.index + 1
                            st.table(df)
                            st.text_area(label="Review", value=response["review"])
                        else:
                            st.error("Error in the table data")
                else:
                    st.write(response)
