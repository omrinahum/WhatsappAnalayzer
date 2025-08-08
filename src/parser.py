"""
Universal WhatsApp chat parser supporting both Hebrew and English formats
"""

import pandas as pd
import re
from datetime import datetime

def parse_whatsapp(file_path):
    """ Parsing data according to Whatsapp exoprting format"""
    # Containts tuples of datetime, user, and message
    chat_data = []

    # Hebrew-style datetime format: [5.8.2025, 15:40:24], user: message
    hebrew_pattern = r'\[(\d{1,2}\.\d{1,2}\.\d{4}), (\d{1,2}:\d{2}:\d{2})\] ([^:]+): (.+)'

    # English-style datetime format: [01/08/2024, 0:51:22], user: message (24-hour format)
    english_pattern = r'\[(\d{1,2}/\d{1,2}/\d{4}), (\d{1,2}:\d{2}:\d{2})\] ([^:]+): (.+)'

    system_message_keywords = [
        "הושמט", "omitted", "media omitted", "group created",
        "שינה את שם הקבוצה", "שינתה את שם הקבוצה", "שם הקבוצה שונה",
        "created group", "You changed", "נוצרה הקבוצה", "את\ה",
        "את/ה", "Messages and calls are end-to-end encrypted",
        "ההודעות והשיחות מוצפנות מקצה לקצה"
    ]

    # Read the file line by line
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            for line in file:
                line = line.strip()
                if not line or ':' not in line:
                    continue
                if any(keyword in line for keyword in system_message_keywords):
                    continue

                # Try matching Hebrew pattern first
                hebrew_match = re.match(hebrew_pattern, line)
                if hebrew_match:
                    date_str = hebrew_match.group(1)
                    time_str = hebrew_match.group(2)
                    user = hebrew_match.group(3).strip()
                    message = hebrew_match.group(4).strip()

                    # Skip if message is empty
                    if not message:
                        continue

                    # Convert Hebrew date to datetime object
                    datetime_obj = datetime.strptime(f"{date_str} {time_str}", "%d.%m.%Y %H:%M:%S")

                    chat_data.append({
                        'datetime': datetime_obj,
                        'user': user,
                        'message': message
                    })
                    continue

                # Try matching English pattern
                english_match = re.match(english_pattern, line)
                if english_match:
                    date_str = english_match.group(1)
                    time_str = english_match.group(2)
                    user = english_match.group(3).strip()
                    message = english_match.group(4).strip()

                    # Skip if message is empty
                    if not message:
                        continue

                    # Convert English date to datetime object (DD/MM/YYYY format, 24-hour time)
                    datetime_obj = datetime.strptime(f"{date_str} {time_str}", "%d/%m/%Y %H:%M:%S")

                    chat_data.append({
                        'datetime': datetime_obj,
                        'user': user,
                        'message': message
                    })

        # Create DataFrame
        df = pd.DataFrame(chat_data)
        return df

    except FileNotFoundError:
        print(f"❌ File not found: {file_path}")
        return pd.DataFrame()
    except Exception as e:
        print(f"❌ Error parsing chat: {e}")
        return pd.DataFrame()