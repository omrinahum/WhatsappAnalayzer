"""
UI Components for the streanlit app
"""

import streamlit as st


def load_css():
    """Load custom CSS styles from external file"""
    try:
        with open("styles.css", "r") as f:
            css_content = f.read()
        st.markdown(f"<style>{css_content}</style>", unsafe_allow_html=True)
    except FileNotFoundError:
        st.warning("CSS file not found. Using default styling.")


def render_header():
    """Render the main header section"""
    st.markdown("""
    <div class="main-header">
        <h1 style="margin: 0; font-size: 3rem; font-weight: 700;">
            <span style="color: #ffffff;">📱</span> 
            <span style="background: linear-gradient(135deg, #6ee7b7 0%, #10b981 100%); -webkit-background-clip: text; -webkit-text-fill-color: transparent;">WhatsApp Chat Analyzer</span>
        </h1>
        <p style="margin: 1rem 0 0 0; font-size: 1.2rem; opacity: 0.9; color: #a7f3d0;">Transform your conversations into beautiful insights</p>
    </div>
    """, unsafe_allow_html=True)


def render_sidebar():
    """Render the sidebar with file upload functionality"""
    st.sidebar.markdown("""
    <div style="text-align: center; padding: 1rem 0; background: linear-gradient(135deg, #065f46 0%, #047857 100%); border-radius: 10px; margin-bottom: 1rem;">
        <h3 style="color: white; margin: 0;">📁 Upload Chat File</h3>
        <p style="color: #a7f3d0; margin: 0.5rem 0 0 0; font-size: 0.9rem;">Get started with your analysis</p>
    </div>
    """, unsafe_allow_html=True)
    
    uploaded_file = st.sidebar.file_uploader(
        "Choose a WhatsApp chat .txt file",
        type=['txt'],
        help="Export your WhatsApp chat and upload the .txt file here"
    )
    
    use_sample = st.sidebar.button("🧪 Use Sample Data", help="Try the app with sample data")
    
    return uploaded_file, use_sample


def render_metrics(stats):
    """Render the metrics overview section"""
    st.markdown("### 📊 Chat Overview")
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("📱 Total Messages", f"{stats['total_messages']:,}")
    with col2:
        st.metric("👥 Active Users", stats['total_users'])
    with col3:
        st.metric("📅 Days Active", stats['date_range_days'])
    with col4:
        st.metric("📊 Daily Average", f"{stats['messages_per_day']:.1f}")
    
    st.markdown("<br>", unsafe_allow_html=True)


def render_chat_analysis_tab(results, visualizer_funcs):
    """Render the Chat Analysis tab content (formerly User Analysis)"""
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("#### 🥧 Message Distribution")
        fig = visualizer_funcs['pie_chart'](results['messages_per_user'])
        st.plotly_chart(fig, use_container_width=True)

        st.markdown("#### 📊 Messages per User")
        fig = visualizer_funcs['per_user'](results['messages_per_user'])
        st.plotly_chart(fig, use_container_width=True)
        
        st.markdown("#### 💬 Message Bursts")
        fig = visualizer_funcs['message_bursts'](results['message_bursts'])
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        st.markdown("#### ⏱️ Response Time per User")  
        fig = visualizer_funcs['response_time'](results['avg_response_time_per_user'])
        st.plotly_chart(fig, use_container_width=True)

        st.markdown("#### 📏 Average Message Length")
        fig = visualizer_funcs['avg_length'](results['avg_message_length'])
        st.plotly_chart(fig, use_container_width=True)

        st.markdown("#### 🗣️ Conversation Starters")
        fig = visualizer_funcs['conversation_starters'](results['conversation_starters'])
        st.plotly_chart(fig, use_container_width=True)

    st.markdown("#### 😂 Laughs per User")
    fig = visualizer_funcs['laughs'](results['laughs_per_user'])
    st.plotly_chart(fig, use_container_width=True)
    
    # Additional insights
    with st.expander("🔍 Additional Insights"):
        st.markdown("#### 💬 Chat Statistics")
        most_active = max(results['messages_per_user'], key=results['messages_per_user'].get)
        most_bursts = max(results['message_bursts'], key=results['message_bursts'].get) if results['message_bursts'] else "None"
        most_starters = max(results['conversation_starters'], key=results['conversation_starters'].get) if results['conversation_starters'] else "None"
        
        st.markdown(f"""
        - **Most Active User:** {most_active}
        - **User with Most Bursts:** {most_bursts}
        - **Top Conversation Starter:** {most_starters}
        - **Total Users:** {results['basic_stats']['total_users']}
        - **Chat Duration:** {results['basic_stats']['date_range_days']} days
        - **Daily Average:** {results['basic_stats']['messages_per_day']:.1f} messages/day
        """)

def render_user_analysis_tab(results, visualizer_funcs):
    """Render the Individual User Analysis tab with user selector"""
    st.markdown("#### 👤 Select User for Individual Analysis")
    
    # User selector
    users = list(results['messages_per_user'].keys())
    selected_user = st.selectbox("Choose a user:", users, key="user_selector")
    
    if selected_user:
        # Get pre-calculated user data (no recomputation needed!)
        user_data = results['all_users_data'][selected_user]
        
        # User metrics (all pre-calculated)
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.metric("📱 Messages", f"{user_data['total_messages']:,}")
        with col2:
            st.metric("📏 Avg Length", f"{user_data['avg_length']:.1f}")
        with col3:
            st.metric("😊 Emojis", f"{user_data['emoji_count']:,}")
        with col4:
            st.metric("😂 Laughs", f"{user_data['laugh_count']:,}")
        
        col5, col6 = st.columns(2)
        with col5:
            st.metric("💬 Message Bursts", f"{user_data['burst_count']:,}")
        with col6:
            st.metric("🗣️ Conversations Started", f"{user_data['starter_count']:,}")
        
        # User activity patterns
        st.markdown("#### 📊 Activity Patterns")
        col1, col2 = st.columns(2)
        
        with col1:
            # User's hourly activity (pre-calculated)
            st.markdown("##### 🕒 Activity by Hour")
            fig = visualizer_funcs['by_hour'](user_data['hourly_activity'])
            st.plotly_chart(fig, use_container_width=True)
            
        with col2:
            # User's emoji usage (pre-calculated)
            if user_data['emoji_count'] > 0:
                st.markdown("##### 😊 Emoji Usage")
                from collections import Counter
                emoji_counts = Counter(user_data['user_emojis']).most_common(10)
                fig = visualizer_funcs['most_common_emojis'](emoji_counts)
                st.plotly_chart(fig, use_container_width=True)
            else:
                st.info("This user hasn't used any emojis yet!")
        
        # User insights
        with st.expander("🔍 User Insights"):
            # Calculate user's share of conversation
            total_chat_messages = sum(results['messages_per_user'].values())
            user_percentage = (user_data['total_messages'] / total_chat_messages) * 100
            
            # Find user's most active hour from pre-calculated data
            hourly_data = user_data['hourly_activity']
            most_active_hour = max(hourly_data.keys(), key=lambda k: hourly_data[k]) if hourly_data else "N/A"
            
            st.markdown(f"""
            **{selected_user}'s Chat Profile:**
            - **Contribution:** {user_percentage:.1f}% of all messages
            - **Most Active Hour:** {most_active_hour}:00
            - **Average Response Time:** {user_data['response_time']}
            - **Communication Style:** {"Emoji-heavy" if user_data['emoji_count'] > user_data['total_messages'] * 0.05 else "Text-focused"}
            """)

def render_words_emojis_tab(results, visualizer_funcs):
    """Render the Words & Emojis tab content (formerly Word Analysis)"""
    col1, col2 = st.columns(2)
    
    with col1:
        if results['most_common_words']:
            st.markdown("#### 🔤 Most Common Words")
            fig = visualizer_funcs['common_words'](results['most_common_words'])
            st.plotly_chart(fig, use_container_width=True)
        else:
            st.info("No common words found in the analysis")
    
    with col2:
        if results['most_common_emojis']:
            st.markdown("#### 😊 Most Common Emojis")
            fig = visualizer_funcs['most_common_emojis'](results['most_common_emojis'])
            st.plotly_chart(fig, use_container_width=True)
        else:
            st.info("No emojis found in the chat")
    
    st.markdown("#### 😊 Emoji Usage per User")
    if results['emoji_per_user']:
        fig = visualizer_funcs['emoji_per_user'](results['emoji_per_user'])
        st.plotly_chart(fig, use_container_width=True)
    else:
        st.info("No emoji usage data available")


def render_time_analysis_tab(results, visualizer_funcs):
    """Render the Time Patterns tab content"""
    st.markdown("#### 🕒 Activity by Hour")
    fig = visualizer_funcs['by_hour'](results['messages_by_hour'])
    st.plotly_chart(fig, use_container_width=True)
    
    # Show top active hours
    hours_sorted = sorted(results['messages_by_hour'].items(), key=lambda x: x[1], reverse=True)
    st.markdown("#### 🔥 Most Active Hours")
    for i, (hour, count) in enumerate(hours_sorted[:5]):
        st.markdown(f"**{i+1}.** {hour:02d}:00 - {count:,} messages")

def render_landing_page():
    """Render the landing page when no file is uploaded"""
    st.markdown("""
    ## 🚀 Welcome to WhatsApp Chat Analyzer
    
    Transform your WhatsApp conversations into beautiful insights and visualizations!
    
    ### 📋 How to get started:
    
    1. **📱 Export your WhatsApp chat:**
       - Open WhatsApp on your phone
       - Go to the chat you want to analyze
       - Tap the three dots → More → Export chat
       - Choose "Without Media" and save as .txt file
    
    2. **📁 Upload your file:**
       - Use the file uploader in the sidebar
       - Or try our sample data to see how it works
    
    3. **📊 Explore your insights:**
       - User activity patterns
       - Message timing analysis
       - Most common words
       - Hebrew text fully supported
    
    ### ✨ Features:
    - 📊 **Interactive Charts** - Zoom, hover, and explore
    - 🇮🇱 **Hebrew Support** - Perfect text rendering
    - 📱 **Mobile Friendly** - Works on any device
    - 🎨 **Beautiful Visualizations** - Professional-grade charts
    - 📈 **Deep Analytics** - Comprehensive chat insights
    """)
    
    st.info("👈 **Get started by uploading a chat file or trying our sample data!**")
    
   
