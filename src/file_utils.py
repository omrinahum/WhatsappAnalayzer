"""
File handling utilities 
"""

import streamlit as st
import os
from parser import parse_whatsapp


def load_chat_data(uploaded_file, use_sample):
    """Load chat data from uploaded file or sample data with caching"""
    try:
        # Create cache key based on file content/sample flag
        if use_sample:
            cache_key = "sample_data"
            file_path = "conversation_sample.txt"
            
            if not os.path.exists(file_path):
                return None, None, "❌ Sample file not found!"
        else:
            # Create cache key from file content hash
            file_content = uploaded_file.getbuffer()
            cache_key = f"uploaded_{hash(bytes(file_content))}"
            file_path = "temp_chat.txt"
            
            # Save uploaded file temporarily (only if not cached)
            if cache_key not in st.session_state.get('parse_cache', {}):
                with open(file_path, "wb") as f:
                    f.write(file_content)

        # Initialize parse cache if doesn't exist
        if 'parse_cache' not in st.session_state:
            st.session_state.parse_cache = {}
        
        # Check if already parsed
        if cache_key in st.session_state.parse_cache:
            df = st.session_state.parse_cache[cache_key]
            success_msg = f"✅ {'Sample data loaded' if use_sample else f'Uploaded {uploaded_file.name}'} (cached)"
            return df, success_msg, None
        
        # Parse file (only if not cached)
        with st.spinner("📄 Parsing chat file..."):
            df = parse_whatsapp(file_path)
            
            # Cache the parsed DataFrame
            st.session_state.parse_cache[cache_key] = df
            
            success_msg = f"✅ {'Sample data loaded' if use_sample else f'Uploaded {uploaded_file.name}'}"
            return df, success_msg, None
            
    except Exception as e:
        return None, None, f"❌ Error loading file: {str(e)}"


def validate_chat_data(df):
    """Validate that the chat data is not empty"""
    if df is None:
        return False, "❌ Failed to load chat data!"
    
    if df.empty:
        return False, "❌ No messages found in the chat file!"
    
    return True, None
