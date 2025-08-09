"""
Analyzing functions the analyze the data
"""

import emoji
import pandas as pd
from collections import Counter
import re
import emoji

def preprocess_df(df: pd.DataFrame) -> pd.DataFrame:
    """Preprocess dataframe with all needed columns for the analyzing process"""
    df = df.copy()
    # Converting the messages to string
    df['message'] = df['message'].astype(str)
    # New columns: lowercase message, message length, hour, day name
    df['lower_message'] = df['message'].str.lower()
    df['message_length'] = df['message'].str.len()
    df['hour'] = df['datetime'].dt.hour
    df['day_name'] = df['datetime'].dt.day_name()

    # Emoji extraction
    def extract_emojis(text):
        """Extract emoji characters from text using emoji package"""
        try:
            emojis_in_text = []
            for char in str(text):
                if emoji.is_emoji(char):
                    emojis_in_text.append(char)
            return emojis_in_text
        except Exception:
            return []
        
    df['emojis'] = df['message'].apply(extract_emojis)
    df['emoji_count'] = df['emojis'].apply(len)
        
    return df

def calculate_basic_stats(df: pd.DataFrame):
    """Calculate basic statistics from the DataFrame"""
    total_messages = len(df)
    total_users = df['user'].nunique()
    date_range = (df['datetime'].max() - df['datetime'].min()).days + 1
    return total_messages, total_users, date_range

def calculate_user_metrics(df: pd.DataFrame):
    """Calculate user-related metrics"""
    messages_per_user = df['user'].value_counts()
    avg_length_per_user = df.groupby('user')['message_length'].mean().round(1)
    return messages_per_user, avg_length_per_user

def calculate_time_patterns(df: pd.DataFrame):
    """Calculate time-based patterns"""
    # Calculate messages by hour and day
    messages_by_hour = df['hour'].value_counts().sort_index()
    messages_by_day = df['day_name'].value_counts()
    # Sort DataFrame by datetime and calculate average response time
    df_sorted = df.sort_values('datetime')
    df_sorted['time_diff'] = df_sorted['datetime'].diff()
    avg_response_time = df_sorted['time_diff'].mean()
    return messages_by_hour, messages_by_day, avg_response_time

def calculate_laugh_analysis(df: pd.DataFrame):
    """Calculate laugh patterns for both Hebrew and English, based on common patterns"""
    # For each message searching for 'חחח', 'ha ha', 'lol', 'lmao' patterns
    pattern = r'ח{3,}|(ha){2,}|lol|lmao'
    df['laughs'] = df['lower_message'].apply(lambda msg: len(re.findall(pattern, msg)))
    laughs_per_user = df.groupby('user')['laughs'].sum().sort_values(ascending=False)
    return laughs_per_user

def calculate_word_frequency(df: pd.DataFrame):
    """Calculate most common words"""
    # Converting all the messages to one long text
    text = ' '.join(df['lower_message'])
    # Define Hebrew and English stopwords that wont be a common word
    stopwords = {
        'את', 'של', 'על', 'כל', 'לא', 'זה', 'אם', 'או', 'כן', 'לו', 'הוא', 'היא', 'אני', 'אתה', 'זו', 'מה', 'איך',
        'מי', 'למה', 'איפה', 'מתי', 'עם', 'בלי', 'אבל', 'גם', 'רק', 'כבר', 'עוד', 'פה', 'שם', 'הם', 'אנחנו', 'אתם',
        'לי', 'שלי', 'שלך', 'שלנו', 'שלכם', 'שלהם', 'שלהן', 'סבבה', 'אז', 'טוב', 'אין', 'יש', 'לך', 'כי', 'איתך',
        'עכשיו', 'שיחה', 'קולית', 'היום', 'כאילו', 'יהיה', 'איזה', 'נראה', 'היה',
        'the', 'and', 'is', 'on', 'to', 'you', 'a', 'i', 'of', 'in', 'it', 'this', 'that', 'for', 'was', 'with', 'are',
        'at', 'but', 'be', 'have', 'not', 'we', 'they', 'he', 'she'
    }

    # Using regex to find words over 2 characters, allowing Hebrew and English letters
    words = re.findall(r'[א-תa-zA-Z]{2,}', text)
    # Filtering out stopwords and returning top 10 most common words
    filtered = [w for w in words if w not in stopwords]
    return Counter(filtered).most_common(10)

def get_avg_response(df: pd.DataFrame):
    """Calculate average response time per user"""
    # Sort DataFrame by datetime
    df_sorted = df.sort_values('datetime').reset_index(drop=True)
    response_times = {}

    # Calculate response times between users
    for i in range(1, len(df_sorted)):
        prev_user = df_sorted.loc[i - 1, 'user']
        curr_user = df_sorted.loc[i, 'user']
        # Excluding messages from the same user
        if prev_user != curr_user:
            time_diff = df_sorted.loc[i, 'datetime'] - df_sorted.loc[i - 1, 'datetime']
            response_times.setdefault(curr_user, []).append(time_diff)

    # Formatting timedelta for better display
    def format_td(td: pd.Timedelta) -> str:
        total = int(td.total_seconds())
        h, rem = divmod(total, 3600)
        m, s = divmod(rem, 60)
        return f"{h}h {m}m {s}s" if h else f"{m}m {s}s" if m else f"{s}s"

    # Returns a dictionary with average response times of each user
    return {
        user: format_td(sum(times, pd.Timedelta(0)) / len(times))
        for user, times in response_times.items()
    }

def calculate_emoji_analysis(df: pd.DataFrame):
    """Calculate emoji usage statistics per user using emoji package"""
    emoji_per_user = df.groupby('user')['emoji_count'].sum().sort_values(ascending=False)
    
    # Get most common emojis overall - now with accurate detection
    all_emojis = []
    for emojis in df['emojis']:
        all_emojis.extend(emojis)
    
    most_common_emojis = Counter(all_emojis).most_common(10)
    
    return emoji_per_user, most_common_emojis

def calculate_message_bursts(df: pd.DataFrame, burst_threshold_minutes=5, min_burst_size=3):
    """Calculate message burst patterns - when users send multiple messages quickly"""
    df_sorted = df.sort_values('datetime').reset_index(drop=True)
    burst_counts = {}
    
    for user in df['user'].unique():
        user_messages = df_sorted[df_sorted['user'] == user]['datetime'].reset_index(drop=True)
        
        if len(user_messages) < min_burst_size:
            burst_counts[user] = 0
            continue
            
        bursts = 0
        current_burst_size = 1
        
        for i in range(1, len(user_messages)):
            time_diff = (user_messages.iloc[i] - user_messages.iloc[i-1]).total_seconds() / 60
            
            if time_diff <= burst_threshold_minutes:
                current_burst_size += 1
            else:
                if current_burst_size >= min_burst_size:
                    bursts += 1
                current_burst_size = 1
        
        # Check if the last sequence was a burst
        if current_burst_size >= min_burst_size:
            bursts += 1
            
        burst_counts[user] = bursts
    
    return pd.Series(burst_counts).sort_values(ascending=False)

def calculate_conversation_starters(df: pd.DataFrame, inactivity_threshold_hours=2):
    """Calculate who starts conversations after periods of inactivity"""
    df_sorted = df.sort_values('datetime').reset_index(drop=True)
    conversation_starters = {}
    
    for i in range(1, len(df_sorted)):
        prev_time = df_sorted.loc[i-1, 'datetime']
        curr_time = df_sorted.loc[i, 'datetime']
        curr_user = df_sorted.loc[i, 'user']
        
        time_diff = (curr_time - prev_time).total_seconds() / 3600  # Convert to hours
        
        if time_diff >= inactivity_threshold_hours:
            conversation_starters.setdefault(curr_user, 0)
            conversation_starters[curr_user] += 1
    
    return pd.Series(conversation_starters).sort_values(ascending=False)

def analyze_chat(df: pd.DataFrame):
    """Analyze WhatsApp chat DataFrame and return statistics, using the functions above"""
    if df.empty:
        return {}

    df = preprocess_df(df)
    total_messages, total_users, date_range = calculate_basic_stats(df)
    messages_per_user, avg_length_per_user = calculate_user_metrics(df)
    messages_by_hour, messages_by_day, avg_response_time = calculate_time_patterns(df)
    laughs_per_user = calculate_laugh_analysis(df)
    most_common_words = calculate_word_frequency(df)
    avg_response_time_per_user = get_avg_response(df)
    emoji_per_user, most_common_emojis = calculate_emoji_analysis(df)
    message_bursts = calculate_message_bursts(df)
    conversation_starters = calculate_conversation_starters(df)
    
    # Pre-calculate all user analysis data 
    all_users_data = calculate_all_user_analysis(
        messages_per_user.to_dict(),
        emoji_per_user.to_dict(),
        laughs_per_user.to_dict(),
        message_bursts.to_dict(),
        conversation_starters.to_dict(),
        avg_response_time_per_user,
        df
    )

    return {
        'basic_stats': {
            'total_messages': total_messages,
            'total_users': total_users,
            'date_range_days': date_range,
            'messages_per_day': round(total_messages / date_range, 1),
            'avg_response_time': avg_response_time
        },
        'messages_per_user': messages_per_user.to_dict(),
        'avg_message_length': avg_length_per_user.to_dict(),
        'messages_by_hour': messages_by_hour.to_dict(),
        'messages_by_day': messages_by_day.to_dict(),
        'most_common_words': most_common_words,
        'avg_response_time_per_user': avg_response_time_per_user,
        'laughs_per_user': laughs_per_user.to_dict(),
        'emoji_per_user': emoji_per_user.to_dict(),
        'most_common_emojis': most_common_emojis,
        'message_bursts': message_bursts.to_dict(),
        'conversation_starters': conversation_starters.to_dict(),
        'all_users_data': all_users_data
    }

def calculate_all_user_analysis(messages_per_user_dict, emoji_per_user_dict, laughs_per_user_dict, 
                                message_bursts_dict, conversation_starters_dict, avg_response_time_dict,
                                df_for_processing):
    """Pre-calculate all user-specific analysis to avoid repeated computation"""
    all_users_data = {}
    
    for user in messages_per_user_dict.keys():
        # Filter user data
        user_df = df_for_processing[df_for_processing['user'] == user]
        
        if user_df.empty:
            all_users_data[user] = {
                'total_messages': 0,
                'avg_length': 0,
                'hourly_activity': {},
                'user_emojis': []
            }
            continue
        
        # Calculate metrics
        total_messages = len(user_df)
        avg_length = user_df['message_length'].mean()
        hourly_activity = user_df.groupby('hour').size().to_dict()
        
        # Get user emojis
        user_emojis = []
        for emojis in user_df['emojis']:
            user_emojis.extend(emojis)
        
        all_users_data[user] = {
            'total_messages': total_messages,
            'avg_length': avg_length,
            'hourly_activity': hourly_activity,
            'user_emojis': user_emojis,
            'emoji_count': emoji_per_user_dict.get(user, 0),
            'laugh_count': laughs_per_user_dict.get(user, 0),
            'burst_count': message_bursts_dict.get(user, 0),
            'starter_count': conversation_starters_dict.get(user, 0),
            'response_time': avg_response_time_dict.get(user, 'N/A')
        }
    
    return all_users_data