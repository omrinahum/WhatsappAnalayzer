""" 
Visualization functions, as go.Figure graphs
"""

import plotly.graph_objects as go
import plotly.express as px
from hebrew_utils import fix_hebrew, fix_dict_keys

# Global constants - defined once, used everywhere
COLORS = ['#54a0ff', '#4ecdc4', "#45bcd1", '#96ceb4', '#feca57', '#ff9ff3', "#54ebff", '#5f27cd']
PRIMARY_GREEN = '#10b981'
ACCENT_GREEN = '#059669'

# Common layout settings
COMMON_LAYOUT = {
    'plot_bgcolor': 'rgba(0,0,0,0)',
    'paper_bgcolor': 'rgba(0,0,0,0)',
    'height': 400,
    'showlegend': False,
    'font': {'family': "Segoe UI, Arial", 'size': 12, 'color': 'white'}
}

AXIS_STYLE = {
    'tickfont': {'size': 13, 'color': 'white', 'family': "Segoe UI"},
    'gridcolor': 'rgba(255,255,255,0.2)',
    'zeroline': False
}

TEXT_STYLE = {
    'size': 14, 
    'color': 'white', 
    'family': "Segoe UI", 
    'weight': "bold"
}

# ----Helper functions:----
# Standardized looking for the graphs

def create_axis_title(text):
    """Create standardized axis title"""
    return {'text': text, 'font': {'size': 16, 'color': 'white', 'family': "Segoe UI", 'weight': "bold"}}

def prepare_user_data(data_dict):
    """Standard user data preparation"""
    # Fixing keys and Hebrew text using HebrewUtils
    data = fix_dict_keys(data_dict)
    users = list(data.keys())
    values = list(data.values())
    fixed_users = [fix_hebrew(user) for user in users]
    return fixed_users, values

def create_bar_chart(x_data, y_data, colors=None, text_data=None, hover_template="", orientation='v'):
    """Create standardized bar chart"""
    if colors is None:
        colors = COLORS[:len(x_data)]

    # Setting style for bars depends on orientation variable
    # vertical
    if orientation == 'v':
        return go.Bar(
            x=x_data, y=y_data,
            marker={'color': colors, 'line': {'color': 'rgba(255,255,255,0.8)', 'width': 3}},
            text=text_data or y_data,
            textposition='auto',
            textfont=TEXT_STYLE,
            hovertemplate=hover_template
        )
    else:  # horizontal
        return go.Bar(
            y=x_data, x=y_data, orientation='h',
            marker={'color': colors, 'line': {'color': 'rgba(255,255,255,0.8)', 'width': 2}},
            text=text_data or y_data,
            textposition='auto',
            textfont=dict(TEXT_STYLE, size=12),
            hovertemplate=hover_template
        )

def create_standard_layout(x_title, y_title, **kwargs):
    """Create standardized layout"""
    layout = COMMON_LAYOUT.copy()
    layout.update({
        'xaxis': dict(AXIS_STYLE, title=create_axis_title(x_title)),
        'yaxis': dict(AXIS_STYLE, title=create_axis_title(y_title), showgrid=True),
        'margin': {'l': 60, 'r': 60, 't': 30, 'b': 100}
    })
    layout.update(kwargs)
    return layout

# ----Visualization functions:----
# Returns go.Figure for to the streamlit app

def get_fig_messages_by_hour(messages_by_hour: dict) -> go.Figure:
    """Create a line chart showing messages by hour of the day"""
    hours = list(messages_by_hour.keys())
    counts = list(messages_by_hour.values())

    fig = go.Figure(data=[
        go.Scatter(
            x=hours, y=counts,
            mode='lines+markers',
            line={'color': PRIMARY_GREEN, 'width': 4, 'shape': 'spline'},
            marker={'color': ACCENT_GREEN, 'size': 8, 'line': {'color': 'white', 'width': 2}},
            fill='tonexty',
            fillcolor='rgba(16, 185, 129, 0.1)',
            text=counts,
            textposition='top center',
            textfont=dict(TEXT_STYLE, size=12),
            hovertemplate='<b>Hour:</b> %{x}:00<br><b>Messages:</b> %{y}<extra></extra>'
        )
    ])
    
    fig.update_layout(create_standard_layout("Hour of Day", "Number of Messages", margin={'l': 60, 'r': 60, 't': 30, 'b': 60}))
    return fig

def get_fig_messages_per_user(messages_per_user: dict) -> go.Figure:
    """Create a bar chart showing messages per user"""
    fixed_users, counts = prepare_user_data(messages_per_user)
    
    fig = go.Figure(data=[
        create_bar_chart(
            fixed_users, counts,
            hover_template='<b>User:</b> %{x}<br><b>Messages:</b> %{y}<extra></extra>'
        )
    ])
    
    fig.update_layout(create_standard_layout("Users", "Number of Messages", 
                                           xaxis={'tickangle': 45, **AXIS_STYLE, 'title': create_axis_title("Users")}))
    return fig

def get_fig_avg_message_length(avg_length_per_user: dict) -> go.Figure:
    """Create a bar chart showing average message length per user"""
    fixed_users, avg_lengths = prepare_user_data(avg_length_per_user)
    
    fig = go.Figure(data=[
        create_bar_chart(
            fixed_users, avg_lengths,
            text_data=[f"{length:.1f}" for length in avg_lengths],
            hover_template='<b>User:</b> %{x}<br><b>Avg Length:</b> %{y:.1f} chars<extra></extra>'
        )
    ])
    
    fig.update_layout(create_standard_layout("Users", "Average Length (characters)", 
                                           xaxis={'tickangle': 45, **AXIS_STYLE, 'title': create_axis_title("Users")}))
    return fig

def get_fig_laughs_per_user(laughs_per_user: dict) -> go.Figure:
    fixed_users, counts = prepare_user_data(laughs_per_user)
    
    fig = go.Figure(data=[
        create_bar_chart(
            fixed_users, counts,
            hover_template='<b>User:</b> %{x}<br><b>Laughs:</b> %{y} 😂<extra></extra>'
        )
    ])
    
    fig.update_layout(create_standard_layout("Users", "Number of Laughs", 
                                           xaxis={'tickangle': 45, **AXIS_STYLE, 'title': create_axis_title("Users")}))
    return fig

def get_fig_most_common_words(common_words: list[tuple[str, int]]) -> go.Figure: 
    """Create a bar chart showing the most common words"""
    if not common_words:
        return go.Figure()
    
    words_dict = dict(common_words[:10])
    data = fix_dict_keys(words_dict)
    words = list(data.keys())
    counts = list(data.values())
    fixed_words = [fix_hebrew(word) for word in words]
    
    fig = go.Figure(data=[
        create_bar_chart(
            fixed_words, counts,
            colors=[PRIMARY_GREEN] * len(words),
            # Make an horizontal bar chart
            orientation='h',
            hover_template='<b>Word:</b> %{y}<br><b>Count:</b> %{x}<extra></extra>'
        )
    ])
    
    fig.update_layout(create_standard_layout("Frequency", "Words", 
                                           height=500,
                                           margin={'l': 120, 'r': 60, 't': 30, 'b': 60},
                                           yaxis={'categoryorder': 'total ascending', **AXIS_STYLE, 'title': create_axis_title("Words")}))
    return fig

def get_fig_messages_pie_chart(messages_per_user: dict) -> go.Figure:
    """Create a pie chart showing message distribution per user"""
    fixed_users, counts = prepare_user_data(messages_per_user)
    
    # Filter out small percentages, under 2%
    total_messages = sum(counts)
    filtered_users, filtered_counts = [], []
    other_count = 0
    
    for user, count in zip(fixed_users, counts):
        if (count / total_messages) * 100 >= 2.0:
            filtered_users.append(user)
            filtered_counts.append(count)
        else:
            other_count += count
    
    if other_count > 0:
        filtered_users.append("Others")
        filtered_counts.append(other_count)
    
    fig = go.Figure(data=[
        go.Pie(
            labels=filtered_users,
            values=filtered_counts,
            hole=0.4,
            marker={'colors': COLORS[:len(filtered_users)], 'line': {'color': 'rgba(255,255,255,0.8)', 'width': 2}},
            textinfo='label+percent',
            textfont=dict(TEXT_STYLE, size=12),
            hovertemplate='<b>%{label}</b><br>Messages: %{value}<br>Percentage: %{percent}<extra></extra>',
            pull=[0.02] * len(filtered_users),
            sort=False
        )
    ])
    
    fig.update_layout({
        **COMMON_LAYOUT,
        'margin': {'l': 20, 'r': 150, 't': 30, 'b': 20},
        'showlegend': True,
        'legend': {
            'orientation': "v", 'yanchor': "middle", 'y': 0.5,
            'xanchor': "left", 'x': 1.01,
            'font': {'size': 12, 'family': "Segoe UI", 'color': 'white'}
        }
    })
    return fig

def get_fig_response_time_per_user(avg_response_time_per_user: dict) -> go.Figure:
    """Create a bar chart showing average response time per user"""
    fixed_users, times = prepare_user_data(avg_response_time_per_user)
    
    def time_to_minutes(time_str):
        """Convert a time string in the format 'Xh Ym' to minutes."""
        minutes = 0
        if 'h' in time_str:
            hours = int(time_str.split('h')[0])
            minutes += hours * 60
            time_str = time_str.split('h')[1].strip()
        if 'm' in time_str:
            mins = int(time_str.split('m')[0].strip())
            minutes += mins
        return minutes

    # Convert all time strings to minutes- eg '1h 30m' -> 90
    time_values = [time_to_minutes(time_str) for time_str in times]
    
    fig = go.Figure(data=[
        create_bar_chart(
            fixed_users, time_values,
            text_data=times,
            hover_template='<b>User:</b> %{x}<br><b>Response Time:</b> %{text}<extra></extra>'
        )
    ])
    
    fig.update_layout(create_standard_layout("Users", "Response Time (minutes)", 
                                           xaxis={'tickangle': 45, **AXIS_STYLE, 'title': create_axis_title("Users")}))
    return fig

def get_fig_emoji_per_user(emoji_per_user: dict) -> go.Figure:
    """Create a bar chart showing emoji usage per user"""
    fixed_users, counts = prepare_user_data(emoji_per_user)
    
    fig = go.Figure(data=[
        create_bar_chart(
            fixed_users, counts,
            hover_template='<b>User:</b> %{x}<br><b>Emojis:</b> %{y} 😊<extra></extra>'
        )
    ])
    
    fig.update_layout(create_standard_layout("Users", "Number of Emojis Used", 
                                           xaxis={'tickangle': 45, **AXIS_STYLE, 'title': create_axis_title("Users")}))
    return fig

def get_fig_most_common_emojis(most_common_emojis: list[tuple[str, int]]) -> go.Figure:
    """Create a horizontal bar chart showing the most common emojis"""
    if not most_common_emojis:
        return go.Figure()
    
    emojis = [emoji for emoji, count in most_common_emojis[:10]]
    counts = [count for emoji, count in most_common_emojis[:10]]
    
    fig = go.Figure(data=[
        create_bar_chart(
            emojis, counts,
            colors=[PRIMARY_GREEN] * len(emojis),
            orientation='h',
            hover_template='<b>Emoji:</b> %{y}<br><b>Count:</b> %{x}<extra></extra>'
        )
    ])
    
    fig.update_layout(create_standard_layout("Frequency", "Emojis", 
                                           height=500,
                                           margin={'l': 80, 'r': 60, 't': 30, 'b': 60},
                                           yaxis={'categoryorder': 'total ascending', **AXIS_STYLE, 'title': create_axis_title("Emojis")}))
    return fig

def get_fig_message_bursts(message_bursts: dict) -> go.Figure:
    """Create a bar chart showing message burst patterns per user"""
    fixed_users, counts = prepare_user_data(message_bursts)
    
    fig = go.Figure(data=[
        create_bar_chart(
            fixed_users, counts,
            hover_template='<b>User:</b> %{x}<br><b>Message Bursts:</b> %{y} 💬<extra></extra>'
        )
    ])
    
    fig.update_layout(create_standard_layout("Users", "Number of Message Bursts", 
                                           xaxis={'tickangle': 45, **AXIS_STYLE, 'title': create_axis_title("Users")}))
    return fig

def get_fig_conversation_starters(conversation_starters: dict) -> go.Figure:
    """Create a bar chart showing conversation starters per user"""
    fixed_users, counts = prepare_user_data(conversation_starters)
    
    fig = go.Figure(data=[
        create_bar_chart(
            fixed_users, counts,
            hover_template='<b>User:</b> %{x}<br><b>Conversations Started:</b> %{y} 🗣️<extra></extra>'
        )
    ])
    
    fig.update_layout(create_standard_layout("Users", "Conversations Started", 
                                           xaxis={'tickangle': 45, **AXIS_STYLE, 'title': create_axis_title("Users")}))
    return fig