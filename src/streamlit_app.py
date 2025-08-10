"""
Streamlit web interface 
"""

import streamlit as st
import traceback

# Import modules
from analyzer import analyze_chat
from visualizer import (
    get_fig_messages_by_hour,
    get_fig_messages_per_user,
    get_fig_avg_message_length,
    get_fig_laughs_per_user,
    get_fig_most_common_words,
    get_fig_messages_pie_chart,
    get_fig_response_time_per_user,
    get_fig_emoji_per_user,
    get_fig_most_common_emojis,
    get_fig_message_bursts,
    get_fig_conversation_starters
)
from ui_components import (
    load_css,
    render_header,
    render_sidebar,
    render_metrics,
    render_chat_analysis_tab,
    render_user_analysis_tab,
    render_time_analysis_tab,
    render_words_emojis_tab,
    render_landing_page
)
from file_utils import load_chat_data, validate_chat_data


def configure_page():
    """
    Configure Streamlit page settings
    """
    st.set_page_config(
        page_title="WhatsApp Chat Analyzer",
        page_icon="📱",
        layout="wide",
        initial_sidebar_state="expanded"
    )


def get_visualizer_functions():
    """
    Return dictionary of visualizer functions for easy passing
    """
    return {
        'by_hour': get_fig_messages_by_hour,
        'per_user': get_fig_messages_per_user,
        'avg_length': get_fig_avg_message_length,
        'laughs': get_fig_laughs_per_user,
        'common_words': get_fig_most_common_words,
        'pie_chart': get_fig_messages_pie_chart,
        'response_time': get_fig_response_time_per_user,
        'emoji_per_user': get_fig_emoji_per_user,
        'most_common_emojis': get_fig_most_common_emojis,
        'message_bursts': get_fig_message_bursts,
        'conversation_starters': get_fig_conversation_starters
    }


def process_chat_analysis(df):
    """
    Process chat data and return analysis results with session state caching
    """
    # Create a hash of the DataFrame for caching
    df_hash = hash(str(df.shape) + str(df.head().to_string()) + str(df.tail().to_string()))
    
    # Check if we already have this analysis cached
    if 'analysis_cache' not in st.session_state:
        st.session_state.analysis_cache = {}
    
    if df_hash in st.session_state.analysis_cache:
        return st.session_state.analysis_cache[df_hash]
    
    # Show spinner while analyzing
    with st.spinner("📊 Analyzing chat data..."):
        results = analyze_chat(df)
        # Cache the results
        st.session_state.analysis_cache[df_hash] = results
        return results


def render_analysis_tabs(results):
    """
    Render the main analysis tabs
    """
    # Get visualizer functions
    visualizer_funcs = get_visualizer_functions()

    # Create tabs for different analysis sections
    tab1, tab2, tab3, tab4 = st.tabs(["Chat Analysis", "User Analysis", "Time Patterns", "Words & Emojis"])
    
    with tab1:
        render_chat_analysis_tab(results, visualizer_funcs)
    
    with tab2:
        render_user_analysis_tab(results, visualizer_funcs)
    
    with tab3:
        render_time_analysis_tab(results, visualizer_funcs)
    
    with tab4:
        render_words_emojis_tab(results, visualizer_funcs)


def handle_error(error):
    """
    Handle and display errors with debug information
    """
    st.error(f"❌ Error: {str(error)}")
    with st.expander("🐛 Debug Information"):
        st.code(traceback.format_exc())


def main():
    """
    Main application function
    """
    # Configure page
    configure_page()
    
    # Load CSS and render header
    load_css()
    render_header()
    
    # Render sidebar and get user inputs
    uploaded_file, use_sample = render_sidebar()
    
    # Process file if uploaded or sample requested
    if uploaded_file is not None or use_sample:
        try:
            # Load chat data
            df, success_msg, error_msg = load_chat_data(uploaded_file, use_sample)
            
            if error_msg:
                st.error(error_msg)
                return
            
            if success_msg:
                st.sidebar.success(success_msg)
            
            # Validate data
            is_valid, validation_error = validate_chat_data(df)
            if not is_valid:
                st.error(validation_error)
                return
            
            # Analyze chat data
            results = process_chat_analysis(df)
            
            # Display metrics
            render_metrics(results['basic_stats'])
            
            # Render analysis tabs
            render_analysis_tabs(results)
            
        except Exception as e:
            handle_error(e)
    else:
        # Show landing page
        render_landing_page()


if __name__ == "__main__":
    main()