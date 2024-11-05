# Set up and run this Streamlit App
import streamlit as st

from helper_functions import llm
from logics.handle_prompt import process_user_message,conver_to_markdown,return_final_choices

from helper_functions.utility import check_password

from langchain_chroma import Chroma
from langchain_core.documents import Document
from langchain_openai import OpenAIEmbeddings


embeddings = OpenAIEmbeddings()
vector_store = Chroma(
    collection_name="example_collection",
    embedding_function=embeddings,
    persist_directory="./chroma_langchain_db" )

retriever = vector_store.as_retriever(search_type='mmr',search_kwargs={'k': 5, 'fetch_k': 10})




# region <--------- Streamlit App Configuration --------->
st.set_page_config(
    layout="centered",
    page_title="My Streamlit App"
)

# Do not continue if check_password is not True.  
if not check_password():  
    st.stop()
    
# endregion <--------- Streamlit App Configuration --------->

st.title("Streamlit App")

form = st.form(key="form")
form.subheader("User input")

user_prompt = form.text_area("Key in proposal title or summary", height=200)

if form.form_submit_button("Submit"):
    
    st.toast(f"User Input Submitted - {user_prompt}")

    st.divider()

    response = process_user_message(user_prompt)
    st.write('summarising proposal based on language model')
    
    st.write(response)
    
    retriever_documents = retriever.invoke(response)
    mmr_result=conver_to_markdown(retriever_documents)
    
    st.write('getting initial list of reviewers')
    
    
    st.markdown(mmr_result)
    
    markdown_table=mmr_result
    new_query=response
    context='narrow down to only 3 reviewers'
    
    final_table=return_final_choices(context, new_query, markdown_table)
    st.markdown(final_table)
    
    st.divider()


