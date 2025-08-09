"""
Tester for the parser functions.
"""
import pandas as pd
from src.parser import parse_whatsapp

# --- Helpers ---
HE_HEBREW = "[5.8.2025, 15:40:24] יונתן: מה קורה?\n"
HE_HEBREW_2 = "[5.8.2025, 15:41:10] דנה: הכל טוב! 😊\n"
HE_SYSTEM_1 = "[5.8.2025, 15:42:00] Messages and calls are end-to-end encrypted. No one outside of this chat, not even WhatsApp, can read or listen to them.\n"
HE_SYSTEM_2 = "[5.8.2025, 15:42:10] יונתן created group \"חברים\" \n"
EN_ENGLISH = "[01/08/2024, 0:51:22] John: hello there\n"
EN_ENGLISH_2 = "[01/08/2024, 0:52:05] Jane: LOL that's funny 😂\n"

MIXED_CHAT = HE_HEBREW + HE_HEBREW_2 + HE_SYSTEM_1 + HE_SYSTEM_2 + EN_ENGLISH + EN_ENGLISH_2

def test_parse_basic_mixed_formats(tmp_path):
    p = tmp_path / "chat.txt"
    p.write_text(MIXED_CHAT, encoding="utf-8")
    df = parse_whatsapp(str(p))

    # Expected: 4 valid messages (2 Hebrew + 2 English), system lines filtered out
    assert len(df) == 4, f"Expected 4 messages, got {len(df)}"

    # Columns exist
    assert set(df.columns) == {"datetime", "user", "message"}

    # Types
    assert pd.api.types.is_datetime64_any_dtype(df["datetime"])

    # Content checks
    users = df["user"].tolist()
    msgs = df["message"].tolist()

    assert "יונתן" in users and "דנה" in users and "John" in users and "Jane" in users
    assert "מה קורה?" in msgs and "הכל טוב! 😊" in msgs
    assert "hello there" in msgs and "LOL that's funny 😂" in msgs

def test_skip_empty_messages(tmp_path):
    # Line with empty message after colon should be skipped
    data = "[5.8.2025, 15:40:24] יונתן: \n" \
           "[5.8.2025, 15:40:30] דנה: היי\n"
    p = tmp_path / "chat.txt"
    p.write_text(data, encoding="utf-8")
    df = parse_whatsapp(str(p))
    assert len(df) == 1
    assert df.iloc[0]["message"] == "היי"

def test_filter_system_keywords(tmp_path):
    # Lines with common system keywords are dropped
    data = "[5.8.2025, 15:40:24] יונתן: היי\n" \
           "[5.8.2025, 15:41:00] Messages and calls are end-to-end encrypted\n" \
           "[5.8.2025, 15:41:10] יונתן שינה את שם הקבוצה ל\"חברים\"\n" \
           "[01/08/2024, 0:51:22] John: hello\n"
    p = tmp_path / "chat.txt"
    p.write_text(data, encoding="utf-8")
    df = parse_whatsapp(str(p))
    # Only 2 real messages should remain
    assert len(df) == 2
    assert df.iloc[0]["user"] == "יונתן"
    assert df.iloc[1]["user"] == "John"

def test_no_crash_on_missing_file():
    # Should return empty DataFrame on missing file
    df = parse_whatsapp("does_not_exist.txt")
    assert isinstance(df, pd.DataFrame)
    assert df.empty

def test_24h_time_parsing(tmp_path):
    # Ensure 24-hour times parse correctly in both formats
    data = "[5.8.2025, 23:59:59] דנה: לילה טוב\n" \
           "[01/08/2024, 13:05:00] John: afternoon\n"
    p = tmp_path / "chat.txt"
    p.write_text(data, encoding="utf-8")
    df = parse_whatsapp(str(p))
    assert df.iloc[0]["datetime"].hour == 23
    assert df.iloc[1]["datetime"].hour == 13
