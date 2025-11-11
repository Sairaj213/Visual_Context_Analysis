import time
import torch
import streamlit as st
from utils.prompting import create_llava_prompt, create_deepseek_conversation

def generate_response(model, processor, image, model_type):
    start_time = time.perf_counter()
    full_prompt_for_display = ""
    raw_output = ""
    answer = ""

    model.eval()
    with torch.no_grad():
        if model_type == "llava":
            prompt = create_llava_prompt(st.session_state.chat_history)
            full_prompt_for_display = prompt
            inputs = processor(images=image, text=prompt, return_tensors="pt").to(model.device)
            output_ids = model.generate(
                **inputs,
                max_new_tokens=st.session_state.max_new_tokens,
                temperature=st.session_state.temperature if st.session_state.temperature > 0 else None,
                top_p=st.session_state.top_p if st.session_state.temperature > 0 else None,
                repetition_penalty=st.session_state.repetition_penalty,
                do_sample=st.session_state.temperature > 0
            )
            raw_output = processor.decode(output_ids[0], skip_special_tokens=True)
            answer = raw_output.split("ASSISTANT:")[-1].strip()

        elif model_type == "deepseek":

            conversation = create_deepseek_conversation(st.session_state.chat_history, image)
            full_prompt_for_display = str(conversation)
            pil_images = [img for turn in conversation if "images" in turn for img in turn["images"]]
            inputs = processor(conversations=conversation, images=pil_images, force_batchify=True).to(model.device)
            tokenizer = processor.tokenizer
            inputs_embeds = model.prepare_inputs_embeds(**inputs)
            output_ids = model.language_model.generate(
                inputs_embeds=inputs_embeds,
                attention_mask=inputs["attention_mask"],
                pad_token_id=tokenizer.eos_token_id,
                bos_token_id=tokenizer.bos_token_id,
                eos_token_id=tokenizer.eos_token_id,
                max_new_tokens=st.session_state.max_new_tokens,
                do_sample=st.session_state.temperature > 0,
                temperature=st.session_state.temperature if st.session_state.temperature > 0 else None,
                top_p=st.session_state.top_p if st.session_state.temperature > 0 else None,
                repetition_penalty=st.session_state.repetition_penalty,
                use_cache=True
            )
            raw_output = tokenizer.decode(output_ids[0].cpu().tolist(), skip_special_tokens=True)

            answer = raw_output.rsplit("Assistant:", 1)[-1].strip()

    end_time = time.perf_counter()
    inference_time = end_time - start_time
    num_tokens = len(output_ids[0])
    tokens_per_sec = num_tokens / inference_time if inference_time > 0 else 0

    st.session_state.last_run_details = {
        "inference_time": f"{inference_time:.2f}s",
        "tokens_per_sec": f"{tokens_per_sec:.2f} tok/s",
        "full_prompt": full_prompt_for_display,
        "raw_output": raw_output
    }
    return answer
