def create_llava_prompt(chat_history):

    history_parts = []
    for role, message in chat_history:
        if role == "user":
            history_parts.append(f"USER: {message}")
        else:
            history_parts.append(f"ASSISTANT: {message}")
    
    prompt_string = "USER: <image>\n" + "\n".join(history_parts) + "\nASSISTANT:"
    return prompt_string

def create_deepseek_conversation(chat_history, image):

    conversation = []
    image_attached = False
    for role, message in chat_history:
        
        if role == "user" and not image_attached:
            conversation.append({
                "role": "User",
                "content": f"<image_placeholder>{message}",
                "images": [image]
            })
            image_attached = True
        else:
            
            conversation.append({"role": "User" if role == "user" else "Assistant", "content": message})
            
    return conversation