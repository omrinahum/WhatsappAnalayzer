"""
File handling utilities 
"""

import streamlit as st
import os
from parser import parse_whatsapp


def load_chat_data(uploaded_file, use_sample):
    """Load chat data from uploaded file or sample data"""
    try:
        # Using sample data
        if use_sample:
            if os.path.exists("conversation_sample.txt"):
                df = parse_whatsapp("conversation_sample.txt")
                return df, "✅ Sample data loaded!", None
            else:
                return None, None, "❌ Sample file not found!"
        # using uploaded file data
        else:
            # Save uploaded file temporarily
            with open("temp_chat.txt", "wb") as f:
                f.write(uploaded_file.getbuffer())
            df = parse_whatsapp("temp_chat.txt")
            return df, f"✅ Uploaded {uploaded_file.name}", None
            
    except Exception as e:
        return None, None, f"❌ Error loading file: {str(e)}"


def validate_chat_data(df):
    """Validate that the chat data is not empty"""
    if df is None:
        return False, "❌ Failed to load chat data!"
    
    if df.empty:
        return False, "❌ No messages found in the chat file!"
    
    return True, None
