import streamlit as st
import torch
from transformers import (
    AutoProcessor,
    LlavaForConditionalGeneration,
    BitsAndBytesConfig,
    AutoModelForCausalLM
)

try:
    from deepseek_vl.models import VLChatProcessor
except ImportError:
    st.warning("DeepSeek-VL specific libraries not found. Please ensure it is installed if you plan to use the model.")
    VLChatProcessor = None 

@st.cache_resource
def load_model(model_name, model_id, model_type):

    with st.spinner(f"Loading {model_name}... This may take a moment."):
        try:
            if model_type == "llava":

                bnb_config = BitsAndBytesConfig(
                    load_in_4bit=True,
                    bnb_4bit_quant_type="nf4",
                    bnb_4bit_compute_dtype=torch.float16, 
                    bnb_4bit_use_double_quant=True
                )
                processor = AutoProcessor.from_pretrained(model_id)
                model = LlavaForConditionalGeneration.from_pretrained(
                    model_id,
                    quantization_config=bnb_config,
                    device_map="auto",
                    torch_dtype=torch.float16,
                    low_cpu_mem_usage=True
                )
                return model, processor

            elif model_type == "deepseek":

                if VLChatProcessor is None:
                    st.error("DeepSeek-VL library is not available. Cannot load the model.")
                    st.stop()

                bnb_config = BitsAndBytesConfig(
                    load_in_4bit=True,
                    bnb_4bit_quant_type="nf4",
                    bnb_4bit_compute_dtype=torch.bfloat16, 
                    bnb_4bit_use_double_quant=True
                )
                processor = VLChatProcessor.from_pretrained(model_id)
                model = AutoModelForCausalLM.from_pretrained(
                    model_id,
                    quantization_config=bnb_config,
                    torch_dtype=torch.bfloat16,
                    trust_remote_code=True,
                    device_map="auto"
                ).eval()
                return model, processor

            else:
                raise ValueError(f"Unknown model type: {model_type}")

        except Exception as e:
            st.error(f"Fatal error during model loading for '{model_name}': {e}", icon="🚨")
            st.stop()
