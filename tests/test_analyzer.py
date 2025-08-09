"""
Tester for the analyzer functions.
"""
import pandas as pd
from datetime import datetime, timedelta
from src.analyzer import (
    preprocess_df,
    calculate_basic_stats,
    calculate_user_metrics,
    calculate_time_patterns,
    calculate_laugh_analysis,
    calculate_word_frequency,
    get_avg_response,
    calculate_emoji_analysis,
    calculate_message_bursts,
    calculate_conversation_starters,
    analyze_chat,
    calculate_all_user_analysis,
)

# ---------- Helpers ----------

def make_df(rows):
    """
    Helper to construct a DataFrame with required columns.
    rows: list of tuples -> (datetime, user, message)
    """
    return pd.DataFrame(rows, columns=["datetime", "user", "message"])


def small_fixture():
    """
    A small, controlled dataset used across multiple tests.
    Contains two days (Aug 5-6, 2025).
    Users: Alice (3), Bob (2), Charlie (1).
    """
    rows = [
        (datetime(2025, 8, 5, 9, 0, 0),  "Alice",   "בוקר טוב 😊"),
        (datetime(2025, 8, 5, 9, 1, 0),  "Bob",     "morning lol"),
        (datetime(2025, 8, 5, 9, 2, 0),  "Alice",   "חחחח זה מצחיק"),
        (datetime(2025, 8, 5, 12, 0, 0), "Alice",   "See you later"),
        (datetime(2025, 8, 5, 12, 6, 0), "Bob",     "hahaha"),  
        (datetime(2025, 8, 6, 0, 0, 0),  "Charlie", "joining late"),
    ]
    return make_df(rows)


# ---------- Tests ----------

def test_preprocess_df_adds_expected_columns():
    """
    Test the preprocess_df function.
    It should:
      - keep original data
      - add lowercase form, message length, hour, day name
      - extract emojis per character (using emoji.is_emoji)
    """
    df = preprocess_df(small_fixture())
    expected_cols = {"lower_message","message_length","hour","day_name","emojis","emoji_count"}
    assert expected_cols.issubset(df.columns)

    # Type checks
    assert pd.api.types.is_integer_dtype(df["hour"])
    assert pd.api.types.is_integer_dtype(df["message_length"])
    # Emoji count non-negative
    assert (df["emoji_count"] >= 0).all()


def test_calculate_basic_stats_inclusive_date_range():
    """
    Test basic statistics calculation including:
    total messages, total users, date range 
    """
    df = preprocess_df(small_fixture())
    total_messages, total_users, date_range = calculate_basic_stats(df)
    assert total_messages == 6
    assert total_users == 3
    assert date_range == 1 


def test_calculate_user_metrics_counts_and_lengths():
    """
    Test user message counts and average lengths.
    """
    df = preprocess_df(small_fixture())
    messages_per_user, avg_len_per_user = calculate_user_metrics(df)

    # Counts
    assert messages_per_user["Alice"] == 3
    assert messages_per_user["Bob"] == 2
    assert messages_per_user["Charlie"] == 1

    # Average length should be positive numbers
    assert (avg_len_per_user > 0).all()


def test_calculate_time_patterns_and_avg_diff():
    """
    Test time-based message patterns and average response time.
    """
    df = preprocess_df(small_fixture())
    by_hour, by_day, avg_td = calculate_time_patterns(df)

    # Ensure keys exist in hour/day aggregations
    assert 9 in by_hour.index and 12 in by_hour.index
    assert isinstance(avg_td, pd.Timedelta)

    # Mean over 5 diffs = 54000 / 5 = 10800s = 3h
    expected = pd.Timedelta(seconds=10800)
    assert avg_td == expected


def test_calculate_laugh_analysis_regex_no_spaces():
    """
    Testing the laugh analysis regex patterns.
    By implementation: pattern = r'ח{3,}|(ha){2,}|lol|lmao'
    """
    rows = [
        (datetime(2025,8,5,10,0,0), "U", "חח"),      # Should not count      
        (datetime(2025,8,5,10,1,0), "U", "חחחח"),    # Should count
        (datetime(2025,8,5,10,2,0), "U", "hahaha"),   # Should count
        (datetime(2025,8,5,10,3,0), "U", "ha ha ha"), # Should not count
        (datetime(2025,8,5,10,4,0), "U", "LOL and lMaO"), # Should count as 2
    ]
    df = preprocess_df(make_df(rows))
    laughs = calculate_laugh_analysis(df)
    assert laughs["U"] == 4


def test_calculate_word_frequency_stopwords_and_min_length():
    """
    Test the word frequency calculation.
    calculate_word_frequency filters stopwords (Heb/Eng) and uses regex for length >=2 letters.
    Ensure content words remain.
    """
    rows = [
        (datetime(2025,8,5,9,0,0), "U", "the the of של זה זה hello שלום coding"),
        (datetime(2025,8,5,9,1,0), "U", "data the analysis עוד"),
    ]
    df = preprocess_df(make_df(rows))
    common = dict(calculate_word_frequency(df))
    for w in ["hello", "coding", "data", "analysis"]:
        assert w in common


def test_get_avg_response_per_user_format_and_values():
    """
    Test the average response time calculation.
    We construct a precise timeline to know exact answers.
    """
    t0 = datetime(2025,8,5,10,0,0)
    rows = [
        (t0 + timedelta(seconds=0),   "A", "hi"),
        (t0 + timedelta(seconds=30),  "B", "hey"),    # B responds to A: 30s
        (t0 + timedelta(seconds=90),  "B", "more"),   # same user, ignored
        (t0 + timedelta(seconds=150), "A", "ok"),     # A responds to B: 60s (150-90)
        (t0 + timedelta(seconds=180), "C", "yo"),     # C responds to A: 30s (180-150)
        (t0 + timedelta(seconds=600), "B", "later"),  # B responds to C: 420s (600-180) -> avg B = (30+420)/2 = 225s
    ]
    df = preprocess_df(make_df(rows))
    avg = get_avg_response(df)

    assert avg["A"] == "1m 0s"
    assert avg["B"] == "3m 45s"  
    assert avg["C"] == "30s"

    # All values should be strings with h/m/s tokens
    for s in avg.values():
        assert isinstance(s, str) and any(t in s for t in ["h","m","s"])


def test_calculate_emoji_analysis_counts_and_toplist():
    """
    Test the emoji analysis function.
    calculate_emoji_analysis returns:
      - emoji_per_user: sum of per-message emoji_count per user
      - most_common_emojis: top 10 overall
    """
    rows = [
        (datetime(2025,8,5,9,0,0), "A", "hi 😊"),
        (datetime(2025,8,5,9,1,0), "B", "ok 👍🏻"),
        (datetime(2025,8,5,9,2,0), "A", "another 😊😊"),
    ]
    df = preprocess_df(make_df(rows))
    emoji_per_user, most_common = calculate_emoji_analysis(df)
    assert emoji_per_user["A"] >= 2  
    assert emoji_per_user["B"] >= 1
    assert isinstance(most_common, list) and len(most_common) >= 1


def test_calculate_message_bursts_threshold_and_counts():
    """
    Test the message burst calculation.
    calculate_message_bursts groups quick successive messages by SAME user.
    We set:
      - burst_threshold_minutes=5
      - min_burst_size=3  => 3 messages within 5 minutes count as a burst
    Scenario: A has two distinct bursts; B has none.
    """
    t0 = datetime(2025,8,5,9,0,0)
    A = [
        (t0 + timedelta(minutes=0),  "A", "x1"),
        (t0 + timedelta(minutes=2),  "A", "x2"),
        (t0 + timedelta(minutes=4),  "A", "x3"),  # -> burst #1
        (t0 + timedelta(minutes=12), "A", "x4"),
        (t0 + timedelta(minutes=14), "A", "x5"),
        (t0 + timedelta(minutes=16), "A", "x6"),  # -> burst #2
    ]
    B = [
        (t0 + timedelta(minutes=1), "B", "b1"),
        (t0 + timedelta(minutes=7), "B", "b2"),  # spaced out -> no burst
    ]
    df = preprocess_df(make_df(A + B))
    bursts = calculate_message_bursts(df, burst_threshold_minutes=5, min_burst_size=3)
    assert bursts["A"] == 2
    assert bursts.get("B", 0) == 0


def test_calculate_conversation_starters_edge_cases():
    """
    Test the conversation starter calculation.
    conversation starters increment when the gap between consecutive messages >= inactivity_threshold_hours.
    We verify exact edge cases with threshold=2h.
    """
    t0 = datetime(2025,8,5,12,0,0)
    rows = [
        (t0,                             "A", "start"),
        (t0 + timedelta(hours=1),        "B", "within 1h"),      # no starter
        (t0 + timedelta(hours=3),        "A", "after 2h+ gap"),  # starter for A
        (t0 + timedelta(hours=5),        "B", "after 2h+ gap"),  # starter for B
        (t0 + timedelta(hours=6, minutes=59), "C", "1h59m gap"), # no starter
        (t0 + timedelta(hours=9),        "C", ">=2h gap"),       # starter for C
    ]
    df = preprocess_df(make_df(rows))
    starters = calculate_conversation_starters(df, inactivity_threshold_hours=2)
    assert starters["A"] >= 1
    assert starters["B"] >= 1
    assert starters["C"] >= 1


def test_calculate_all_user_analysis_structure_and_values():
    """
    Test the calculation per user.
    calculate_all_user_analysis aggregates per-user stats into a dict.
    We provide minimal dicts so that the function must fall back to defaults for missing users/fields.
    """
    df = preprocess_df(small_fixture())
    # Inputs for user-level aggregation
    messages_per_user = {"Alice": 3, "Bob": 2, "Charlie": 1}
    emoji_per_user = {"Alice": 2, "Bob": 1}          # Charlie missing on purpose
    laughs_per_user = {"Alice": 1, "Bob": 1}
    message_bursts = {"Alice": 1}
    conversation_starters = {"Alice": 1, "Charlie": 1}
    avg_response_time_per_user = {"Alice": "1m 0s", "Bob": "3m 45s"}  # Charlie missing -> 'N/A'

    all_users = calculate_all_user_analysis(
        messages_per_user,
        emoji_per_user,
        laughs_per_user,
        message_bursts,
        conversation_starters,
        avg_response_time_per_user,
        df
    )

    # Structure check
    assert set(all_users.keys()) == {"Alice","Bob","Charlie"}
    for user, data in all_users.items():
        assert {"total_messages","avg_length","hourly_activity","user_emojis","emoji_count","laugh_count","burst_count","starter_count","response_time"}.issubset(data.keys())

    # Specific expectations
    assert all_users["Alice"]["total_messages"] == 3
    assert all_users["Bob"]["emoji_count"] == 1
    assert all_users["Charlie"]["response_time"] == "N/A"  # fallback
    assert isinstance(all_users["Alice"]["hourly_activity"], dict)


def test_analyze_chat_end_to_end_contract():
    """
    analyze_chat should return a dict with all top-level keys,
    and numbers consistent with the small_fixture dataset.
    """
    df = small_fixture()
    result = analyze_chat(df)

    expected_keys = {
        "basic_stats",
        "messages_per_user",
        "avg_message_length",
        "messages_by_hour",
        "messages_by_day",
        "most_common_words",
        "avg_response_time_per_user",
        "laughs_per_user",
        "emoji_per_user",
        "most_common_emojis",
        "message_bursts",
        "conversation_starters",
        "all_users_data",
    }
    assert expected_keys.issubset(result.keys())

    # Basic consistency checks
    assert result["basic_stats"]["total_messages"] == 6
    assert result["basic_stats"]["total_users"] == 3
    assert result["messages_per_user"]["Alice"] == 3
