import streamlit as st
from chat_interface import ChatInterface
from typing import List, Dict, Optional


def initialize_session_state():
    """Initialize session state variables."""
    if "messages" not in st.session_state:
        st.session_state.messages = []
    if "chat_interface" not in st.session_state:
        st.session_state.chat_interface = None

def main():
    st.title("Chat with Dobby AI")
    
    # Initialize session state
    initialize_session_state()
    
    # API key input
    api_key = "fw_3ZRA4aj6HKSXuM6R9RkWhixK" #st.sidebar.text_input("Enter your Fireworks API key:", type="password")
    
    if api_key:
        if st.session_state.chat_interface is None:
            st.session_state.chat_interface = ChatInterface(api_key)
        
        # Display chat messages
        for message in st.session_state.messages:
            with st.chat_message(message["role"]):
                st.write(message["content"])
        
        # Chat input
        if prompt := st.chat_input("What would you like to discuss?"):
            # Add user message to chat history
            st.session_state.messages.append({"role": "user", "content": prompt})
            with st.chat_message("user"):
                st.write(prompt)
            
            # Get bot response
            with st.chat_message("assistant"):
                with st.spinner("Thinking..."):
                    response = st.session_state.chat_interface.get_completion(
                        messages=st.session_state.messages,
                        model="accounts/sentientfoundation/models/dobby-mini-unhinged-llama-3-1-8b#accounts/sentientfoundation/deployments/81e155fc"
                    )
                    st.write(response)
            
            # Add assistant response to chat history
            st.session_state.messages.append({"role": "assistant", "content": response})
    
    else:
        st.warning("Please enter your Fireworks API key in the sidebar to start chatting.")

if __name__ == "__main__":
    main()