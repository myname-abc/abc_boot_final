# Set up and run this Streamlit App
__import__('pysqlite3') 
import sys 
sys.modules['sqlite3'] = sys.modules.pop('pysqlite3')
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


disclaimer="""

IMPORTANT NOTICE: This web application is developed as a proof-of-concept prototype. The information provided here is NOT intended for actual usage and should not be relied upon for making any decisions, especially those related to financial, legal, or healthcare matters.

Furthermore, please be aware that the LLM may generate inaccurate or incorrect information. You assume full responsibility for how you use any generated output.

Always consult with qualified professionals for accurate and personalized advice.

"""

if 'page' not in st.session_state:
    st.session_state.page = 'Home'


page = st.sidebar.radio("Select a Page", ("Home", "About Us", "Methodology"))

st.session_state.page = page

if st.session_state.page == "Home":
    st.title("Welcome to the Home Page")
    st.write("This is the home page of the app.")


    
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
          
          st.write(disclaimer)
          
          st.divider()


elif st.session_state.page == "About Us":
    st.title("About Us")
    markdown_script= """
    **project scope**:
    To identify potential reviewers for any given proposal title / proposal summary 
    
    **objectives**:
    To serve as an additional tool for grants officers to identify potential reviewers, especially when the proposals are technical
    
    **data sources**:
    Self-curated excel sheet contatin the reviewer's info and expertise, saved as vector_store using Chroma
    200+ reviewers across a wide range of disciplines 
    
    **features**:
    LLM is able to provide suggestions on the potential fields/ sub-discipline a proposal would be in 
    Using embedding relevant reviewers can be identified
    From the pool of relevant reviewers, the LLM will recommend the top 3 reviewers
    
    
    """
    
    st.markdown(markdown_script)
    st.divider()
elif st.session_state.page == "Methodology":
    st.title("Methodology")
    st.write("This is an about page where you can describe the project.")
    dot_string = """
                  digraph G {
                      rankdir=TB;
                      node [shape=box];
                      Start -> User_input -> LLM_summarise_&_supplement_Info -> Retrieve_reviewer_entry_from_vector_store -> info_to_markdown_table -> pick_top_3_reviwers -> End;
                  }
                  """

    st.graphviz_chart(dot_string)
    
    markdown_script= """
    **Process Flow**:
    
    1. **Start**
    2. **Step 1**: User types in proposal title or proposal summary 
    3. **Step 2**: LLM will summarise proposal and list down all related disciplines to supplement the search query
    4. **Step 3**: retrieve relevant reviewer from chroma vector_store with MMR
    5. **Step 4**: convert output to markdown table to preserve metadata
    6. **Step 5**: LLM to summarise and choose the top 3 relevant reviewers
    7. **End**
    """
    
    st.markdown(markdown_script)

