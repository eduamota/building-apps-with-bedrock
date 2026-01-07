import streamlit as st
import requests
import json
import os

# API endpoint
API_URL = "https://fz6ys48n9e.execute-api.us-east-1.amazonaws.com/prod"

st.title("S3 Vectors RAG Chat")

# API Key input
api_key = st.sidebar.text_input("API Key", type="password", value=os.getenv("API_KEY", ""))
if not api_key:
    st.warning("Please enter your API key in the sidebar to continue.")
    st.stop()

# Initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display chat messages
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Chat input
if prompt := st.chat_input("Ask a question..."):
    # Add user message to chat history
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # Get response from API
    with st.chat_message("assistant"):
        with st.spinner("Thinking..."):
            try:
                response = requests.post(
                    f"{API_URL}/ask",
                    headers={
                        "Content-Type": "application/json",
                        "x-api-key": api_key
                    },
                    json={"question": prompt}
                )
                
                if response.status_code == 200:
                    data = response.json()
                    if data["success"]:
                        answer = data["answer"]
                        sources = data["sources"]
                        
                        st.markdown(answer)
                        
                        # Show sources
                        if sources:
                            st.markdown("**Sources:**")
                            for source in sources:
                                st.markdown(f"- {source['title']} (Score: {source['score']:.3f})")
                        
                        # Add assistant response to chat history
                        st.session_state.messages.append({"role": "assistant", "content": answer})
                    else:
                        error_msg = f"Error: {data['error']}"
                        st.error(error_msg)
                        st.session_state.messages.append({"role": "assistant", "content": error_msg})
                else:
                    error_msg = f"API Error: {response.status_code}"
                    st.error(error_msg)
                    st.session_state.messages.append({"role": "assistant", "content": error_msg})
                    
            except Exception as e:
                error_msg = f"Connection Error: {str(e)}"
                st.error(error_msg)
                st.session_state.messages.append({"role": "assistant", "content": error_msg})

# Sidebar with app info
with st.sidebar:
    st.header("About")
    st.write("This chat interface uses S3 Vectors for document retrieval and Amazon Nova Pro for generating responses.")
    st.write("**API Authentication:** Secured with API key")
    
    if st.button("Clear Chat"):
        st.session_state.messages = []
        st.rerun()
