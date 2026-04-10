import streamlit as st
import ollama

st.set_page_config(
    page_title="local-llm",
    layout="wide",
    page_icon="◈",
    initial_sidebar_state="expanded"
)

# Custom CSS 
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=DM+Mono:wght@300;400;500&family=DM+Sans:wght@300;400;500&display=swap');

/* Base */
.stApp {
    background-color: #0d0d10 !important;
}

/* Sidebar Styling - Targeted safely */
[data-testid="stSidebar"] {
    background-color: #111115 !important;
    border-right: 1px solid #1e1e26 !important;
}

/* Sidebar Text & Labels */
[data-testid="stSidebar"] p, 
[data-testid="stSidebar"] label {
    font-family: 'DM Mono', monospace !important;
    font-size: 12px !important;
    color: #888899 !important;
    letter-spacing: 0.05em !important;
}

/* Hide Deploy Button and main menu gently */
.stDeployButton {display:none;}
#MainMenu {visibility: hidden;}

/* Main container width */
.block-container {
    max-width: 800px !important;
    padding-top: 2rem !important;
    padding-bottom: 8rem !important;
}

/* Chat Input Styling */
[data-testid="stChatInput"] {
    background-color: #14141a !important;
    border: 1px solid #22222e !important;
    border-radius: 10px !important;
}
[data-testid="stChatInputTextArea"] {
    color: #ccccdd !important;
    font-family: 'DM Sans', sans-serif !important;
}

/* Hide default avatars to use custom ones later if needed */
[data-testid="stChatMessageAvatarUser"],
[data-testid="stChatMessageAvatarAssistant"] {
    display: none !important;
}

/* Custom Scrollbar */
::-webkit-scrollbar { width: 4px; }
::-webkit-scrollbar-track { background: transparent; }
::-webkit-scrollbar-thumb { background: #2a2a35; border-radius: 2px; }
</style>
""", unsafe_allow_html=True)


# ─────────────────────────────────────────────────────────────────────────────
# SIDEBAR
# ─────────────────────────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown(
        "<p style='font-family:DM Mono,monospace;font-size:10px;"
        "letter-spacing:0.2em;color:#55555f;text-transform:uppercase;"
        "margin-bottom:16px;'>Config</p>",
        unsafe_allow_html=True
    )

    selected_model = st.selectbox(
        "Model",
        ["moondream:latest", "gemma4:e2b", "llama3.2"],
        index=1
    )

    st.divider()
    reasoning_on = st.toggle("Reasoning", value=True)
    st.divider()
    temp = st.slider("Temperature", 0.0, 1.5, 0.7, step=0.1)
    max_tokens = st.slider("Max tokens", 128, 2048, 512, step=64)
    st.divider()

    if st.button("Clear history", use_container_width=True):
        st.session_state.messages = []
        st.rerun()

    st.markdown(
        "<div style='margin-top:2rem;display:flex;align-items:center;gap:8px;'>"
        "<div style='width:6px;height:6px;border-radius:50%;background:#1e4030;'></div>"
        "<span style='font-family:DM Mono,monospace;font-size:10px;"
        "color:#2a5540;letter-spacing:0.1em;'>OFFLINE</span>"
        "</div>",
        unsafe_allow_html=True
    )


# ─────────────────────────────────────────────────────────────────────────────
# SESSION STATE & SYSTEM PROMPT
# ─────────────────────────────────────────────────────────────────────────────
if "messages" not in st.session_state:
    st.session_state.messages = []

system_prompt = "You are a chill, helpful local AI assistant."
if not reasoning_on:
    system_prompt += (
        " Do not use <think> tags or internal reasoning."
        " Be concise and friendly. Running offline — minimize token usage."
    )


# ─────────────────────────────────────────────────────────────────────────────
# HEADER
# ─────────────────────────────────────────────────────────────────────────────
st.markdown(
    f"""
    <div style='display:flex; justify-content:space-between; align-items:center;'>
        <p style='font-family:DM Mono,monospace;font-size:16px;color:#ccccdd;margin:0;'>
            LLM-Local <span style='color:#333344;'>◈</span>
        </p>
        <p style='font-family:DM Mono,monospace;font-size:12px;color:#555566;margin:0;'>
            {selected_model}
        </p>
    </div>
    <div style='border-top:1px solid #18181e;margin:12px 0 24px;'></div>
    """,
    unsafe_allow_html=True
)


# ─────────────────────────────────────────────────────────────────────────────
# CHAT HISTORY RENDERER
# ─────────────────────────────────────────────────────────────────────────────
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        if msg["role"] == "user":
            st.markdown(f"<div style='color:#c0c0d0; font-family:DM Sans; text-align:right;'>{msg['content']}</div>", unsafe_allow_html=True)
        else:
            # Handle the <think> tag visually if it exists
            content = msg["content"]
            if "<think>" in content and "</think>" in content:
                parts = content.split("</think>")
                think_part = parts[0].replace("<think>", "").strip()
                answer_part = parts[1].strip()
                
                with st.expander("◦ reasoning"):
                    st.markdown(f"<div style='font-family:DM Mono; font-size:12px; color:#555566;'>{think_part}</div>", unsafe_allow_html=True)
                
                st.markdown(f"<div style='color:#9a9aaa; font-family:DM Sans;'>{answer_part}</div>", unsafe_allow_html=True)
            else:
                st.markdown(f"<div style='color:#9a9aaa; font-family:DM Sans;'>{content}</div>", unsafe_allow_html=True)

if not st.session_state.messages:
    st.markdown(
        "<div style='margin:100px auto 0;text-align:center;'>"
        "<div style='font-family:DM Mono,monospace;font-size:32px;color:#18181e;margin-bottom:16px;'>◈</div>"
        "<p style='font-family:DM Mono,monospace;font-size:12px;color:#333344;letter-spacing:0.1em;'>"
        "running locally<br>no data leaves this machine</p></div>",
        unsafe_allow_html=True
    )


# ─────────────────────────────────────────────────────────────────────────────
# CHAT INPUT + STREAMING
# ─────────────────────────────────────────────────────────────────────────────
if prompt := st.chat_input("What's on your mind?"):

    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(f"<div style='color:#c0c0d0; font-family:DM Sans; text-align:right;'>{prompt}</div>", unsafe_allow_html=True)


    messages_with_system = [{"role": "system", "content": system_prompt}] + st.session_state.messages

        #Stream response
    with st.chat_message("assistant"):
        placeholder = st.empty()
        full_response = ""
        
        try:
            stream = ollama.chat(
                model=selected_model,
                messages=messages_with_system,
                stream=True,
                options={"num_predict": max_tokens, "temperature": temp}
            )

            for chunk in stream:
                token = chunk["message"]["content"]
                full_response += token
                
                # Render the streaming text with the cursor block
                # Using a simple markdown block prevents the UI from duplicating history
                placeholder.markdown(f"<div style='color:#9a9aaa; font-family:DM Sans;'>{full_response}▌</div>", unsafe_allow_html=True)

            # Final render without the cursor
            placeholder.markdown(f"<div style='color:#9a9aaa; font-family:DM Sans;'>{full_response}</div>", unsafe_allow_html=True)
            
            # 4= history
            st.session_state.messages.append({"role": "assistant", "content": full_response})
            st.rerun() # Force a clean rerun to format the <think> tags correctly into expanders
            
        except Exception as e:
            st.error(f"Failed to connect to {selected_model}. Is Ollama running?")