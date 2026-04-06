import streamlit as st
import requests
import uuid
import os
#  UI Configuration 
st.set_page_config(
    page_title="RiskIntel // AI Financial Copilot",
    page_icon="📈",
    layout="wide",
    initial_sidebar_state="expanded"
)


st.markdown("""
    <style>
    /* Global Background and Text */
    .stApp {
        background-color: #0d1117;
        color: #c9d1d9;
    }
    
    /* Header Styling */
    .main-title {
        font-family: 'Inter', sans-serif;
        font-weight: 800;
        font-size: 2.5rem;
        background: -webkit-linear-gradient(45deg, #58a6ff, #3fb950);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin-bottom: 0rem;
    }
    .sub-title {
        color: #8b949e;
        font-size: 1.1rem;
        margin-bottom: 2rem;
    }
    
    /* Hide default Streamlit branding */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    </style>
""", unsafe_allow_html=True)

# Session State Management 
# Generate a unique session ID for the backend memory
if "session_id" not in st.session_state:
    st.session_state.session_id = str(uuid.uuid4())

# Store the chat history for the frontend display
if "messages" not in st.session_state:
    st.session_state.messages = [
        {"role": "assistant", "content": "Welcome to RiskIntel. I am your autonomous financial copilot. Ask me to analyze a stock, compare companies, or evaluate market trends. I will remember our conversation."}
    ]

#  Sidebar Panel 
with st.sidebar:
    st.image("https://img.icons8.com/color/96/000000/line-chart.png", width=60)
    st.markdown("### ⚙️ System Control")
    st.caption(f"**Session ID:** `{st.session_state.session_id[:8]}...`")
    st.caption("**Backend:** `FastAPI + LangGraph`")
    st.caption("**Brain:** `Llama 3.3 70b`")
    st.divider()
    
    # A clear button that resets BOTH the frontend chat and the backend memory
    if st.button("🗑️ Clear Conversation", use_container_width=True):
        st.session_state.messages = [
            {"role": "assistant", "content": "Conversation cleared. What would you like to analyze next?"}
        ]
        # Generate a new session ID so the backend also forgets the history
        st.session_state.session_id = str(uuid.uuid4())
        st.rerun()

#  Main Chat Interface
st.markdown('<p class="main-title">RiskIntel Terminal</p>', unsafe_allow_html=True)
st.markdown('<p class="sub-title">Powered by Agentic RAG, Live Web Search, and Long-Term Memory</p>', unsafe_allow_html=True)
st.divider()

# Display all previous messages in the chat
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Input & API Logic
# Chat input field stays locked to the bottom
if prompt := st.chat_input("e.g., What is Apple's stock price, and how does it compare to Microsoft?"):
    
    # Add user message to state and display it
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # Show assistant thinking state
    with st.chat_message("assistant"):
        message_placeholder = st.empty()
        
        with st.spinner("🤖 Agent is analyzing your request, executing tools, and consulting memory..."):
            try:
                api_url = os.getenv("API_URL", "http://localhost:8000/analyze")
                payload = {
                    "query": prompt,
                    "session_id": st.session_state.session_id
                }
                
                response = requests.post(api_url, json=payload, timeout=90)
                
                if response.status_code == 200:
                    data = response.json()
                    final_answer = data["analysis"]
                    final_answer = final_answer.replace("$", "\$")
                    # Display the final answer
                    message_placeholder.markdown(final_answer)
                    
                    # Add assistant response to state so it stays on screen
                    st.session_state.messages.append({"role": "assistant", "content": final_answer})
                    
                else:
                    error_msg = f" **Backend Error:** System returned code `{response.status_code}`\n\nDetails: `{response.text}`"
                    message_placeholder.error(error_msg)
                    st.session_state.messages.append({"role": "assistant", "content": error_msg})
                    
            except requests.exceptions.Timeout:
                err = " **TIMEOUT:** The agent took too long to think. Try a simpler query."
                message_placeholder.error(err)
            except requests.exceptions.ConnectionError:
                err = " **CONNECTION REFUSED:** Ensure your FastAPI server is running on `localhost:8000` in Terminal 1."
                message_placeholder.error(err)