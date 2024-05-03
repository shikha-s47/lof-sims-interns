import streamlit as st
import markdown2
import json
import requests
from sim_prompts import *  # Ensure this import provides the needed functionality

st.set_page_config(
    page_title='Simulated Case Generator',
    page_icon='🌌',
    layout="wide",
    initial_sidebar_state='collapsed'
)

def llm_call(model, messages):
    response = requests.post(
        url="https://openrouter.ai/api/v1/chat/completions",
        headers={
            "Authorization": "Bearer " + st.secrets["OPENROUTER_API_KEY"],  # Fixed to correct access to secrets
            "Content-Type": "application/json",
            "HTTP-Referer": "https://fsm-gpt-med-ed.streamlit.app",  # To identify your app
            "X-Title": "GPT and Med Ed",
        },
        data=json.dumps({
            "model": model,
            "messages": messages,
        })
    )
    # Extract the response content
    response_data = response.json()
    return response_data # Adjusted to match expected JSON structure

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


if check_password():
    st.info("**Provide inputs and generate a case! Open the left sidebar to change models; default is inexpensive Haiku.**")

    if "response_markdown" not in st.session_state:
        st.session_state["response_markdown"] = ""

    col1, col2, col3 = st.columns([1,1,4])

    with col1:    
        st.info("**Include anything you'd like in the case in the text paragraph, or use the expanded form to generate the case. The AI will generate additional details as needed to complete the case**")
            
        # Profession selection
        # professions = st.multiselect(
        #     "Profession",
        #     [
        #         "Physical Therapy",
        #         "Pathology Assistant",
        #         "Nursing",
        #         "Medicine",
        #         "Nurse Anesthesia",
        #         "Physician Assistant",
        #         "Podiatry",
        #         "Pharmacy",
        #         "Dietician",
        #         "Health Administration",
        #         "Lifestyle Medicine",
        #         "Clinical Psychology",
        #         "Interprofessional Focus",
        #         "Other"
        #     ],
        #     help="Select the profession(s) related to this case study.")
        
        # if "Other" in professions:
        #     other_profession = st.text_input("Other Profession")
        #     professions = professions + [other_profession]
        with st.sidebar:
            model_choice = st.selectbox("Model Options", ("anthropic/claude-3-haiku",
            "anthropic/claude-3-sonnet", "anthropic/claude-3-opus", "openai/gpt-4-turbo", 
            "google/gemini-pro", "meta-llama/llama-2-70b-chat", ), index=0)
            
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

        # Input Type and Learning Objectives
        # input_type = st.radio("Input Type", ["Text Paragraph", "Detailed Input"], horizontal=True, index=0)


        case_study_input = {
            'Case Title': st.text_input("Case Study Title"),
            'Case Description': st.text_area("Case Study Description"),
            'Patient Age': st.number_input("Patient Age", min_value=0, max_value=120, step=1),
            'Patient Legal Sex': st.selectbox("Patient Legal Sex", ["Male", "Female", "Other"]),
            'Patient Race/Ethnicity/Gender Identity/Sexuality': st.text_input("Patient Race/Ethnicity/Gender Identity/Sexuality")  # And the rest of the inputs
        }
        case_study_input = json.dumps(case_study_input)
    # # Standardized Format
    # standardized_format = st.selectbox("Standardized Format", ["Format 1", "Format 2", "Format 3"])
    with col2: 
        st.info("Click submit when ready to generate a case! A download button will appear once generated.")
        submit_button = st.button("Submit")

    if submit_button:
        # Build the message dictionary according to your model's requirements

            
        messages = [{"role": "system", "content": f'Use input provided with additional AI generated content to fully flesh out a clinical case optimized for simulation using the following format: {output_format}'},
        {"role": "user", "content": f"""
            "case_details": {case_study_input},
            "learning_objectives": {learning_objectives},
            """
        }]
    
        # Call the llm_call function with the model and messages as arguments
        response_content = llm_call(model_choice, messages)
        st.session_state.response_markdown = response_content['choices'][0]['message']['content']
    if st.session_state.response_markdown != "":
        with col3:
            with st.container():
            # Display the response from LLM call
                st.success("Case Study Framework Generated!")
                # st.json(response_content)
                
                st.markdown(st.session_state.response_markdown)
        
        with col2:
            html = markdown2.markdown(st.session_state.response_markdown, extras=["tables"])
            st.download_button('Download Followup Response', html, f'followup_response.html', 'text/html')
