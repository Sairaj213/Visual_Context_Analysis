import streamlit as st
import json
import base64
from io import BytesIO

def initialize_session_state():

    defaults = {
        'mode': "💬 Conversational Chat",
        'chat_history': [],
        'analysis_report': {},
        'uploaded_image_A': None,
        'uploaded_image_B': None,
        'system_prompt': "You are a helpful and insightful AI assistant that analyzes images. Your answers should be concise and directly address the user's question.",
        'last_run_details': {},
        'focus_mode': False,
        'max_new_tokens': 256,
        'temperature': 0.2,
        'top_p': 0.9,
        'repetition_penalty': 1.1,
    }
    for key, value in defaults.items():
        if key not in st.session_state:
            st.session_state[key] = value

def get_session_export_data():

    session_data = {key: val for key, val in st.session_state.items()}
    widget_keys_to_exclude = ["uploader_A", "uploader_comp_A", "uploader_comp_B", "importer"]

    for key in widget_keys_to_exclude:
        if key in session_data:
            del session_data[key]

    if session_data.get('uploaded_image_A'):
        image_bytes = session_data['uploaded_image_A'].getvalue()
        session_data['uploaded_image_A'] = base64.b64encode(image_bytes).decode('utf-8')

    if session_data.get('uploaded_image_B'):
        image_bytes = session_data['uploaded_image_B'].getvalue()
        session_data['uploaded_image_B'] = base64.b64encode(image_bytes).decode('utf-8')

    return json.dumps(session_data, indent=2)

def import_session_state(uploaded_file):

    try:
        new_state = json.loads(uploaded_file.getvalue())
        for key, val in new_state.items():

            if key.startswith('uploaded_image') and val:
                st.session_state[key] = BytesIO(base64.b64decode(val))
            else:
                st.session_state[key] = val
        st.success("Session loaded successfully!")
        st.rerun()
    except (json.JSONDecodeError, KeyError, Exception) as e:
        st.error(f"Failed to load session file. Error: {e}")
