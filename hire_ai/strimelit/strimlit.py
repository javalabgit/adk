import streamlit as st
import requests
import json
import os
import uuid
import time

# --- Config ---
st.set_page_config(
    page_title="HIRE AI",
    page_icon="🤖",
    layout="centered",
    menu_items={'About': "Multi-agent system where each agent performs a specific task."}
)

API_BASE_URL = "http://localhost:8000"  # FastAPI server

# --- Initialize session state ---
if "user_id" not in st.session_state:
    st.session_state.user_id = f"user-{uuid.uuid4()}"
if "session_id" not in st.session_state:
    st.session_state.session_id = None
if "messages" not in st.session_state:
    st.session_state.messages = []
if "app_name" not in st.session_state:
    st.session_state.app_name = "custom_agent_creation"
if "agent_display_name" not in st.session_state:
    st.session_state.agent_display_name = "HIRE AI WORKSPACE"
if "uploaded_file" not in st.session_state:
    st.session_state.uploaded_file = None

# --- Create session ---
def create_session():
    session_id = f"s{int(time.time())}"
    response = requests.post(
        f"{API_BASE_URL}/apps/{st.session_state.app_name}/users/{st.session_state.user_id}/sessions/{session_id}",
        headers={"Content-Type": "application/json"},
        data=json.dumps({})
    )
    if response.status_code == 200:
        st.session_state.session_id = session_id
        st.session_state.messages = []
        return True
    else:
        st.error(f"Failed to create session: {response.text}")
        return False

# --- Animate title change ---
def animated_title_change(new_title):
    placeholder = st.empty()
    for dots in ["", ".", "..", "..."]:
        placeholder.markdown(f"## Changing agent{dots}")
        time.sleep(0.2)
    placeholder.markdown(f"## 🤖 Now talking to: **{new_title}**")

# --- Send message ---
def send_message(message):
    if not st.session_state.session_id:
        st.error("Create a session first.")
        return False

    st.session_state.messages.append({"role": "user", "content": message})

    with st.spinner("Waiting for response..."):
        try:
            files = None
            data = {
                "app_name": st.session_state.app_name,
                "user_id": st.session_state.user_id,
                "session_id": st.session_state.session_id,
                "new_message": {
                    "role": "user",
                    "parts": [{"text": message}]
                }
            }

            # Attach file if uploaded
            if st.session_state.uploaded_file:
                uploaded = st.session_state.uploaded_file
                files = {
                    "file": (uploaded["name"], uploaded["content"], uploaded["type"])
                }
                response = requests.post(
                    f"{API_BASE_URL}/run_with_file",
                    data={"payload": json.dumps(data)},
                    files=files,
                    timeout=60
                )
                st.session_state.uploaded_file = None
            else:
                response = requests.post(
                    f"{API_BASE_URL}/run",
                    headers={"Content-Type": "application/json"},
                    data=json.dumps(data),
                    timeout=120
                )

            if response.status_code != 200:
                st.error(f"Error: {response.text}")
                return False

            events = response.json()
            assistant_text = ""

            for event in events:
                content = event.get("content", {})
                parts = content.get("parts", [])
                if content.get("role") == "model" and parts:
                    part = parts[0].get("text", "")
                    assistant_text += part

            if assistant_text:
                st.session_state.messages.append({
                    "role": "assistant",
                    "content": assistant_text
                })

        except Exception as e:
            st.error(f"Error: {str(e)}")
            return False

    return True

# --- Get available agents ---
def get_agents(path):
    os.makedirs(path, exist_ok=True)  # Ensure directory exists
    try:
        return [name for name in os.listdir(path) if os.path.isdir(os.path.join(path, name))]
    except Exception as e:
        st.error(f"Error loading agents: {e}")
        return []

# --- Agent selection sidebar ---
def new_agent():
    with st.sidebar:
        st.markdown("### 🤖 Select Agent")

        folders_path = "./hire_ai"
        folders = get_agents(folders_path)
        folders = [f for f in folders if f not in ["__pycache__", "strimelit","hire_ai","hire_ai_project"]]

        # Styling
        st.markdown("""
        <style>
        .agent-button {
            background-color: #f0f2f6;
            color: #31333F;
            padding: 0.6em 1em;
            border-radius: 0.5em;
            border: 1px solid #e0e0e0;
            margin-bottom: 0.5em;
            font-weight: 500;
            transition: all 0.2s ease-in-out;
            width: 100%;
            display: block;
            text-align: left;
        }
        .agent-button:hover {
            background-color: #dbeafe;
        }
        .active-agent {
            background-color: #c7f7cc !important;
            font-weight: bold;
        }
        </style>
        """, unsafe_allow_html=True)

        for folder in folders:
            display_name = folder.replace("_", " ").title()
            is_active = (folder == st.session_state.app_name)
            css_class = "agent-button active-agent" if is_active else "agent-button"

            if st.button(display_name, key=f"agent-{folder}"):
                st.session_state.app_name = folder
                st.session_state.agent_display_name = display_name
                create_session()
                animated_title_change(display_name)
                st.rerun()

        st.divider()
        st.markdown("Create a New Agent 🤖")
        if st.button("Create"):
            st.session_state.app_name = "custom_agent_creation"
            st.session_state.agent_display_name = "Agent Creator 🤖"
            create_session()
            st.rerun()

        st.divider()
        st.markdown("### Session")
        if st.session_state.session_id:
            st.success(f"Active session: `{st.session_state.session_id}`")
            if st.button("🔄 New Session"):
                create_session()
                st.rerun()
        else:
            st.warning("No active session")
            if st.button("➕ Create Session"):
                create_session()
                st.rerun()

        st.divider()
        st.caption("This assistant is powered by a FastAPI backend.")

# --- Header ---
st.markdown(f"## 🤖 Now talking to: **{st.session_state.agent_display_name}**")

# --- Chat Display ---
st.subheader("Conversation")
for msg in st.session_state.messages:
    if msg["role"] == "user":
        st.chat_message("user").write(msg["content"])
    else:
        with st.chat_message("assistant"):
            content = msg["content"]
            if content.startswith("data:image"):
                st.image(content)
            elif content.endswith((".png", ".jpg", ".jpeg", ".webp")):
                st.image(content)
            else:
                st.markdown(content, unsafe_allow_html=True)

# --- Agent and session controls ---
new_agent()

# --- File uploader (small UI) ---
with st.expander("📎 Upload Media", expanded=False):
    uploaded_file = st.file_uploader(
        "Upload File", 
        type=["png", "jpg", "jpeg", "pdf", "txt", "csv", "json"], 
        label_visibility="collapsed"
    )
    if uploaded_file:
        st.session_state.uploaded_file = {
            "name": uploaded_file.name,
            "type": uploaded_file.type,
            "content": uploaded_file.read()
        }
        st.success(f"Uploaded: {uploaded_file.name}")

# --- Chat input ---
if st.session_state.session_id:
    user_input = st.chat_input("Type your question...")
    if user_input:
        send_message(user_input)
        st.rerun()
else:
    st.info("🤖 Select an Agent to begin.")
