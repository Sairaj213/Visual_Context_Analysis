import streamlit as st
from utils.session import get_session_export_data, import_session_state
from config import MODELS 

def build_sidebar():

    if st.session_state.focus_mode:
        return

    with st.sidebar:
        st.header("🔬 Configuration")
        st.toggle("Focus Mode", key="focus_mode", help="Hide this sidebar for an immersive view.")

        st.markdown("### 🧠 Model Selection")
        model_options = list(MODELS.keys())
        selected_model_name = st.radio(
            "Choose a Vision-Language Model:",
            model_options,
            key="selected_model_name",
            on_change=handle_model_change 
        )
        st.session_state.model_config = MODELS[selected_model_name]

        st.markdown("---")

        if st.session_state.mode != "🖼️ Image Comparison":
            uploaded_file_A = st.file_uploader("Upload an image", type=['png', 'jpg', 'jpeg'], key="uploader_A")
            if uploaded_file_A:
                if st.session_state.uploaded_image_A is None or uploaded_file_A.getvalue() != st.session_state.uploaded_image_A.getvalue():
                    st.session_state.uploaded_image_A = uploaded_file_A
                    st.session_state.chat_history = []
                    st.session_state.analysis_report = {}
        else:
            st.subheader("Image Comparison")
            uploaded_file_A = st.file_uploader("Upload Image A", type=['png', 'jpg', 'jpeg'], key="uploader_comp_A")
            uploaded_file_B = st.file_uploader("Upload Image B", type=['png', 'jpg', 'jpeg'], key="uploader_comp_B")
            if uploaded_file_A: st.session_state.uploaded_image_A = uploaded_file_A
            if uploaded_file_B: st.session_state.uploaded_image_B = uploaded_file_B

        with st.expander("⚙️ Fine-Tune Generation", expanded=False):
            st.text_area("System Prompt (Note: LLaVA-specific)", key="system_prompt", height=150, help="This system prompt is primarily used by LLaVA. DeepSeek-VL follows a different conversational structure.")
            st.slider("Max Tokens", 10, 2048, key="max_new_tokens")
            st.slider("Temperature", 0.0, 1.5, 0.05, key="temperature")
            st.slider("Top-p (Nucleus)", 0.0, 1.0, 0.05, key="top_p")
            st.slider("Repetition Penalty", 1.0, 2.0, 0.05, key="repetition_penalty")

        st.markdown("---")
        st.subheader("Session Management")

        if st.button("Export Session", use_container_width=True):
            session_json = get_session_export_data()
            st.download_button(
                label="Download Session File",
                data=session_json,
                file_name="visual_suite_session.json",
                mime="application/json",
                use_container_width=True
            )
        imported_file = st.file_uploader("Import Session File", type=['json'], key="importer")
        if imported_file:
            import_session_state(imported_file)

        st.markdown("---")
        st.info(f"**Active Model:** `{st.session_state.model_config['id']}`\n\n**Quantization:** `4-bit`")

def handle_model_change():

    from core.model_loader import load_model
    load_model.clear()
    st.session_state.chat_history = []
    st.session_state.analysis_report = {}
    st.success(f"Model switched to {st.session_state.selected_model_name}. Chat history has been cleared.")
