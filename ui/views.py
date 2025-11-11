import streamlit as st
from PIL import Image
from core.inference import generate_response
from utils.helpers import combine_images

def run_conversational_chat(model, processor, model_type):

    st.subheader("💬 Conversational Chat")

    for role, message in st.session_state.chat_history:
        with st.chat_message(role):
            st.markdown(message)

    if user_question := st.chat_input("Ask a follow-up question..."):

        st.session_state.chat_history.append(("user", user_question))
        with st.chat_message("user"):
            st.markdown(user_question)

        with st.chat_message("assistant"):
            with st.spinner("Thinking..."):
                image = Image.open(st.session_state.uploaded_image_A).convert("RGB")
                # No longer need to pass user_question separately
                answer = generate_response(model, processor, image, model_type)
                st.markdown(answer)
                st.session_state.chat_history.append(("assistant", answer))

def run_deep_analysis(model, processor, model_type):

    st.subheader("🔬 Deep Analysis")
    col1, col2 = st.columns(2)

    prompts = {
        "Object Detection": "List all objects in the image with detailed descriptions.",
        "Scene & Mood": "Describe the overall mood, setting, and atmosphere of the scene.",
        "Action & Intent": "What are the subjects doing, and what might their intentions be?",
        "Inference & Prediction": "Based on the scene, what is likely to happen next?"
    }
    creative_prompts = {
        "Write a Short Story": "Write a one-paragraph story inspired by this scene.",
        "Suggest a Title": "Suggest five creative and fitting titles for this image.",
        "Create a Dialogue": "If the subjects could talk, write a short dialogue for them."
    }

    def run_analysis(p_key, p_val):
        with st.spinner(f"Running {p_key}..."):
            image = Image.open(st.session_state.uploaded_image_A).convert("RGB")
            st.session_state.chat_history = [("user", p_val)]
            st.session_state.analysis_report[p_key] = generate_response(model, processor, image, model_type)

    with col1:
        st.markdown("##### Analytical Toolkit")
        for p_key, p_val in prompts.items():
            if st.button(f"Analyze {p_key}", use_container_width=True):
                run_analysis(p_key, p_val)

        st.markdown("##### Creative Toolkit")
        for p_key, p_val in creative_prompts.items():
            if st.button(f"Generate: {p_key}", use_container_width=True):
                 run_analysis(p_key, p_val)

    with col2:
        st.markdown("##### Analysis Report")
        if not st.session_state.analysis_report:
            st.info("Click an analysis button on the left to generate a report.")
        else:
            for analysis_type, report in st.session_state.analysis_report.items():
                with st.expander(f"📄 {analysis_type} Report", expanded=True):
                    st.markdown(report)

def run_comparison_mode(model, processor, model_type):

    st.subheader("🖼️ Image Comparison")
    if not (st.session_state.uploaded_image_A and st.session_state.uploaded_image_B):
        st.warning("Please upload both Image A and Image B in the sidebar.")
        return

    for role, message in st.session_state.chat_history:
        with st.chat_message(role):
            st.markdown(message)

    if user_question := st.chat_input("Ask a question comparing the images..."):

        full_question = f"The user has provided two images combined side-by-side (Image A on the left, Image B on the right). Please answer the following question comparing them: {user_question}"
        st.session_state.chat_history.append(("user", full_question))
        with st.chat_message("user"):
            st.markdown(user_question)

        with st.chat_message("assistant"):
            with st.spinner("Comparing and thinking..."):
                combined_image = combine_images(st.session_state.uploaded_image_A, st.session_state.uploaded_image_B)
                answer = generate_response(model, processor, combined_image, model_type)
                st.markdown(answer)
                st.session_state.chat_history.append(("assistant", answer))

def run_engine_room_tab():

    st.subheader("⚙️ Engine Room: Last Run Details")
    if not st.session_state.last_run_details:
        st.info("No inference has been run yet.")
        return

    details = st.session_state.last_run_details
    col1, col2 = st.columns(2)
    col1.metric("Inference Time", details.get('inference_time', 'N/A'))
    col2.metric("Tokens/Second", details.get('tokens_per_sec', 'N/A'))

    with st.expander("Full Prompt Sent to Model", expanded=False):
        st.code(details.get('full_prompt', 'N/A'), language='text')
    with st.expander("Raw Model Output", expanded=False):
        st.code(details.get('raw_output', 'N/A'), language='text')
