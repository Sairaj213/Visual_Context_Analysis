import streamlit as st
from config import PAGE_TITLE, PAGE_ICON, MODELS
from core.model_loader import load_model
from utils.session import initialize_session_state
from ui.sidebar import build_sidebar
from ui.views import (
    run_conversational_chat,
    run_deep_analysis,
    run_comparison_mode,
    run_engine_room_tab
)

def main():

    st.set_page_config(layout="wide", page_title=PAGE_TITLE, page_icon=PAGE_ICON)
    initialize_session_state()

    if 'selected_model_name' not in st.session_state:
        st.session_state.selected_model_name = list(MODELS.keys())[0]

    st.session_state.model_config = MODELS[st.session_state.selected_model_name]
    model_config = st.session_state.model_config
    model, processor = load_model(
        st.session_state.selected_model_name,
        model_config['id'],
        model_config['type']
    )
    model_type = model_config['type']

    st.title(f"{PAGE_ICON} Visual Analysis Suite")
    build_sidebar()

    if st.session_state.uploaded_image_A is None and st.session_state.mode != "🖼️ Image Comparison":
        st.info("Please upload an image via the sidebar to begin analysis.", icon="☝️")
        return

    main_cols = st.columns([0.45, 0.55] if not st.session_state.focus_mode else [0.4, 0.6])

    with main_cols[0]:
        st.subheader("🖼️ Visual Context")
        if st.session_state.mode != "🖼️ Image Comparison":
            if st.session_state.uploaded_image_A:
                st.image(st.session_state.uploaded_image_A, use_container_width=True)
        else:
            if st.session_state.uploaded_image_A:
                st.image(st.session_state.uploaded_image_A, caption="Image A", use_container_width=True)
            if st.session_state.uploaded_image_B:
                st.image(st.session_state.uploaded_image_B, caption="Image B", use_container_width=True)

    with main_cols[1]:
        st.radio(
            "Select Mode:",
            ["💬 Conversational Chat", "🔬 Deep Analysis", "🖼️ Image Comparison"],
            horizontal=True,
            key="mode"
        )

        interaction_tab, engine_tab = st.tabs(["[ Interaction ]", "[ ⚙️ Engine Room ]"])

        with interaction_tab:
            if st.session_state.mode == "💬 Conversational Chat":
                run_conversational_chat(model, processor, model_type)
            elif st.session_state.mode == "🔬 Deep Analysis":
                run_deep_analysis(model, processor, model_type)
            else:
                run_comparison_mode(model, processor, model_type)

        with engine_tab:
            run_engine_room_tab()

if __name__ == "__main__":
    main()
