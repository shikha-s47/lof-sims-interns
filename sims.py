import streamlit as st
import markdown2
import json
import requests
from sim_prompts import *  # Ensure this import provides the needed functionality

from sqlalchemy import create_engine, Column, Integer, String, Text, MetaData, Index
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# Database setup
DATABASE_URL = "sqlite:///app_data.db"  # SQLite database

engine = create_engine(DATABASE_URL)
Session = sessionmaker(bind=engine)
session = Session()
Base = declarative_base()

# Define the models
class Transcript(Base):
    __tablename__ = 'transcripts'
    id = Column(Integer, primary_key=True, autoincrement=True)
    content = Column(Text, nullable=False)
    role = Column(String, nullable=False)
    specialty = Column(String, nullable=True)
    __table_args__ = (Index('transcript_content_idx', 'content'),)

class Assessment(Base):
    __tablename__ = 'assessments'
    id = Column(Integer, primary_key=True, autoincrement=True)
    content = Column(Text, nullable=False)
    role = Column(String, nullable=False)
    specialty = Column(String, nullable=True)
    __table_args__ = (Index('assessment_content_idx', 'content'),)

class CaseDetails(Base):
    __tablename__ = 'case_details'
    id = Column(Integer, primary_key=True, autoincrement=True)
    saved_name = Column(String, nullable=False)
    content = Column(Text, nullable=False)
    role = Column(String, nullable=False)
    specialty = Column(String, nullable=True)
    __table_args__ = (Index('case_details_content_idx', 'content'),)

# Create tables
Base.metadata.create_all(engine)

st.set_page_config(
    page_title='Simulated Case Generator',
    page_icon='🌌',
    layout="wide",
    initial_sidebar_state='collapsed'
)

def init_session():
    if "final_case" not in st.session_state:
        st.session_state["final_case"] = ""
        
# Function to save a transcript
def save_transcript(transcript_content, role, specialty):
    new_transcript = Transcript(content=transcript_content, role=role, specialty=specialty)
    session.add(new_transcript)
    session.commit()

# Function to save an assessment
def save_assessment(assessment_content, role, specialty):
    new_assessment = Assessment(content=assessment_content, role=role, specialty=specialty)
    session.add(new_assessment)
    session.commit()

# Function to save case details
def save_case_details(case_details_content, saved_name, role, specialty):
    new_case_details = CaseDetails(content=case_details_content, saved_name=saved_name, role=role, specialty=specialty)
    session.add(new_case_details)
    session.commit()

# Function to retrieve records with full-text search and wildcards
def get_records(model, search_text=None, saved_name=None, role=None, specialty=None):
    query = session.query(model)
    if search_text:
        search_text = f"%{search_text}%"  # Wildcard search
        query = query.filter(model.content.ilike(search_text))
    if saved_name:
        saved_name = f"%{saved_name}%"  # Wildcard search
        query = query.filter(model.saved_name.ilike(saved_name))
    if role:
        query = query.filter_by(role=role)
    if specialty:
        query = query.filter_by(specialty=specialty)
    return query.all()

def llm_call(model, messages):
    response = requests.post(
        url="https://openrouter.ai/api/v1/chat/completions",
        headers={
            "Authorization": "Bearer " + st.secrets["OPENROUTER_API_KEY"],  # Fixed to correct access to secrets
            "Content-Type": "application/json",
            "HTTP-Referer": "https://fsm-gpt-med-ed.streamlit.app",  # To identify your app
            "X-Title": "lof-sims",
        },
        data=json.dumps({
            "model": model,
            "messages": messages,
        })
    )
    # Extract the response content
    response_data = response.json()
    return response_data  # Adjusted to match expected JSON structure

def check_password():
    """Returns `True` if the user had the correct password."""

    def password_entered():
        """Checks whether a password entered by the user is correct."""
        if st.session_state["password"] == st.secrets["password"]:
            st.session_state["password_correct"] = True
            del st.session_state["password"]  # don't store password
        else:
            st.session_state["password_correct"] = False

    if "password_correct" not in st.session_state:
        # First run, show input for password.
        st.text_input(
            "Password", type="password", on_change=password_entered, key="password"
        )
        st.write("*Please contact David Liebovitz, MD if you need an updated password for access.*")
        return False
    elif not st.session_state["password_correct"]:
        # Password not correct, show input + error.
        st.text_input(
            "Password", type="password", on_change=password_entered, key="password"
        )
        st.error("😕 Password incorrect")
        return False
    else:
        # Password correct.
        return True

st.title("Case Study Framework Generator")
init_session()

if check_password():
    st.info("**Provide inputs and generate a case! Open the left sidebar to change models; default is inexpensive Haiku.**")

    if "response_markdown" not in st.session_state:
        st.session_state["response_markdown"] = ""
        
    if "expanded" not in st.session_state:
        st.session_state["expanded"] = True
        
    tab1, tab2 = st.tabs(["New Case", "Retrieve a Case"])
    
    with tab1:

        col1, col2, col3 = st.columns([1, 0.5, 4])

        with col1:    
            st.info("**Include desired history in the text paragraph. The AI will generate additional details as needed to draft an educational case.**")
                
            with st.sidebar:
                model_choice = st.selectbox("Model Options", (
                    "anthropic/claude-3-haiku",
                    "anthropic/claude-3-sonnet", 
                    "anthropic/claude-3-opus", 
                    "openai/gpt-4-turbo", 
                    "google/gemini-pro", 
                    "meta-llama/llama-2-70b-chat",
                ), index=0)
                
            learning_objectives = st.multiselect(
                "Select one or more learning objectives; default is a focused history/examination",
                [
                    "Perform a focused history and examination",
                    "Provide patient education",
                    "Demonstrate effective interpersonal skills",
                    "Determine a Dx and DDx",
                    "Determine a plan for management",
                    "Document the patient case"
                ], default="Perform a focused history and examination",
                help="Choose the learning objectives relevant to this case study."
            )

            case_study_input = {
                'Case Title': st.text_input("Case Study Title"),
                'Case Description': st.text_area("Case Study Description, as detailed or brief as desired, e.g., 65F with acute chest pain...", height=200),
                'Case Primary Diagnosis': st.text_input("Case Primary Diagnosis, e.g., Pulmonary Embolism"),
            }
            case_study_input = json.dumps(case_study_input)
        
        with col1: 
            st.info("Click submit when ready to generate a case! A download button will appear in the next column once generated.")
            submit_button = st.button("Submit")

        if submit_button:
            messages = [
                {"role": "system", "content": f'Use input provided with additional AI generated content to fully flesh out a clinical case optimized for simulation using the following format: {output_format}'},
                {"role": "user", "content": f"""
                    "case_details": {case_study_input},
                    "learning_objectives": {learning_objectives},
                    """
                }
            ]
        
            with col2:
                with st.spinner("Assembling Case... Please wait."):
                    response_content = llm_call(model_choice, messages)
            st.session_state.response_markdown = response_content['choices'][0]['message']['content']
        if st.session_state.response_markdown != "":
            with col3:
                st.success("Case Study Framework Generated!")
                with st.expander("View Full Case", expanded=st.session_state.expanded):
                    st.markdown(st.session_state.response_markdown)
                    st.session_state.expanded = False
            
            with col2:
                st.info("Download or edit the case and begin the simulator!")
                html = markdown2.markdown(st.session_state.response_markdown, extras=["tables"])
                st.download_button('Download the Case', html, f'case.html', 'text/html')
            
                if st.checkbox("Edit Case (Scroll Down)", value=False):
                    with col3:
                        st.session_state.expanded = False
                        st.warning("Please edit the case as needed while leaving other characters, e.g., '#' and '*', in place. Enter control-enter or command-enter to save edits!")
                        
                        st.session_state["final_case"] = st.text_area("Edit Case, enter control-enter or command-enter to save edits!", st.session_state.response_markdown, height=1000) 
                else:
                    st.session_state["final_case"] = st.session_state.response_markdown

                if st.session_state["final_case"] != "":
                    if st.button("Send case to the simulator!"):
                        st.page_link("pages/🧠_Sim_Chat.py", label="Click Here to Wake the Simulator", icon="🧠")

        with col3:
            roles = ["1st year medical student", "2nd year medical student", "3rd year medical student", "4th year medical student", "Resident", "Fellow", "Attending"]
            if st.session_state.final_case:
                case_details = st.text_area("Case Details", value=st.session_state.final_case)
                saved_name = st.text_input("Saved Name (Required to save case)")
                selected_role = st.selectbox("Role", roles)
                specialty = ""
                if selected_role in ["Resident", "Fellow", "Attending"]:
                    specialty = st.text_input("Specialty", "")

                if st.button("Save Case to the Database to use Again"):
                    st.warning("You may need to click a second time to view the message that it was saved!")
                    if saved_name:
                        save_case_details(case_details, saved_name, selected_role, specialty)
                        st.success("Case Details saved successfully!")
                    else:
                        st.error("Saved Name is required to save the case")

    with tab2:
        st.header("Retrieve Records")
        search_text = st.text_input("Search Text")
        search_saved_name = st.text_input("Search by Saved Name")
        search_role = st.selectbox("Search by Role", [""] + roles)
        search_specialty = ""
        if search_role in ["Resident", "Fellow", "Attending"]:
            search_specialty = st.text_input("Search by Specialty", "")

        if st.button("Search Cases"):
            case_details = get_records(CaseDetails, search_text, search_saved_name, search_role, search_specialty)

            st.subheader("Case Details")
            for i, c in enumerate(case_details):
                st.write(f"Saved Name: {c.saved_name}, Role: {c.role}, Specialty: {c.specialty}")
                st.write(c.content)
                if st.button(f"Select Case {i+1}", key=f"select_case_{i}"):
                    st.session_state.final_case = c.content
                    st.success(f"Case {i+1} selected and saved to session state!")
