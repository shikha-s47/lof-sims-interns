import streamlit as st
from sim_prompts import *
import markdown2
from groq import Groq


@st.cache_data
def extract_patient_door_chart_section(text):
    """
    Extracts the PATIENT DOOR CHART section from the given text string and returns it.
    
    Args:
    - text (str): The input text containing multiple sections, including "PATIENT DOOR CHART".
    
    Returns:
    - str: The extracted "PATIENT DOOR CHART" section through the end of the provided text.
    """
    # Define the start marker for the section to extract
    start_marker = "## PATIENT DOOR CHART"
    
    # Find the position where the relevant section starts
    start_index = text.find(start_marker)
    
    # If the section is found, extract and return the text from that point onwards
    if start_index != -1:
        return text[start_index:]
    else:
        # Return a message indicating the section was not found if it doesn't exist in the string
        return "PATIENT DOOR CHART section not found in the provided text."
# st.write(f'Here is the case {st.session_state.final_case}')

try:
    extracted_section = extract_patient_door_chart_section(st.session_state.final_case)
    st.info(extracted_section)
    if "messages" not in st.session_state:
        st.session_state.messages = [{"role": "system", "content": f'{sim_persona} Here are the specifics for your persona: {st.session_state.final_case}'}, ]
except Exception as e:
    st.error(f"Please return to the main page. An error occurred. Please do not 're-load' when in the middle of a conversation. Here are the error details: {e}. ")



#################################################

# Set OpenAI API key from Streamlit secrets
groq_client = Groq(api_key = st.secrets['GROQ_API_KEY'])

# st.set_page_config(
#     page_title='Fast Helpful Chat',
#     page_icon='🌌',
#     initial_sidebar_state='expanded'
# )
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
def parse_groq_stream(stream):
    for chunk in stream:
        if chunk.choices:
            if chunk.choices[0].delta.content is not None:
                yield chunk.choices[0].delta.content

st.title("Clinical Simulator Chat")
# st.caption('Powered by [Groq](https://groq.com/).')


if check_password():
    st.info("Enter your questions at the bottom of the page!")
    
    st.sidebar.title('Customization')
    st.session_state.model = st.sidebar.selectbox(
            'Choose a model',
            ['llama3-70b-8192', 'llama3-8b-8192', 'mixtral-8x7b-32768', 'gemma-7b-it']
        )
        # Initialize chat history

        
    # if st.sidebar.checkbox("Change personality? (Will clear history.)"):
    #     persona = st.sidebar.radio("Pick the persona", ("Regular user", "Physician"), index=1)
    #     if persona == "Regular user":
    #         system = st.sidebar.text_area("Make your own system prompt or use as is:", value=system_prompt2)
    #     else:
    #         system = system_prompt
    #     st.session_state.messages = [{"role": "system", "content": system}]
        
    if "sim_response" not in st.session_state:
        st.session_state["sim_response"] = ""



    # Display chat messages from history on app rerun
    for message in st.session_state.messages:
        if message["role"] == "user":
            with st.chat_message(message["role"], avatar="👩‍💻"):
                st.markdown(message["content"])
        elif message["role"] == "assistant":
            with st.chat_message(message["role"], avatar="🤖"):
                st.markdown(message["content"])

    # Accept user input
    if prompt := st.chat_input("What's up?"):
        # Add user message to chat history
        st.session_state.messages.append({"role": "user", "content": prompt})
        # Display user message in chat message container
        with st.chat_message("user", avatar="👩‍💻"):
            st.markdown(prompt)
            
            # Display assistant response in chat message container
        with st.chat_message("assistant", avatar="🤖"):        
            stream = groq_client.chat.completions.create(
                model=st.session_state["model"],
                messages=[
                    {"role": m["role"], "content": m["content"]}
                    for m in st.session_state.messages
                ],
                temperature=0.3,
                stream=True,
            )
            st.session_state.sim_response = st.write_stream(parse_groq_stream(stream))
            
            
            
        st.session_state.messages.append({"role": "assistant", "content": st.session_state.sim_response})

    if st.session_state["sim_response"]:
        conversation_str = ""
        for message in st.session_state.messages:
            if message["role"] == "user":
                conversation_str += "👩‍💻: " + message["content"] + "\n\n"
            elif message["role"] == "assistant":
                conversation_str += "🤖: " + message["content"] + "\n\n"
        html = markdown2.markdown(conversation_str, extras=["tables"])
        st.download_button('Download the conversation when done!', html, f'sim_response.html', 'text/html')
    
    if st.sidebar.button("Clear chat history"):
        st.session_state.messages = []