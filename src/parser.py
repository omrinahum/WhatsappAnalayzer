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

    # English-style datetime format: [8/5/25, 3:40:24 PM], user: message
    english_pattern = r'\[(\d{1,2}/\d{1,2}/\d{2,4}), (\d{1,2}:\d{2}:\d{2}) ([APap][Mm])\] ([^:]+): (.+)'

    # Read the file line by line
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            for line in file:
                line = line.strip()

                if not line:
                    continue

                # Skip system messages like "media omitted"
                if 'הושמט' in line or 'omitted' in line.lower():
                    continue

                # Try matching Hebrew pattern
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
                    am_pm = english_match.group(3).upper()
                    user = english_match.group(4).strip()
                    message = english_match.group(5).strip()

                    # Skip if message is empty
                    if not message:
                        continue

                    # Convert English date to datetime object 
                    datetime_obj = datetime.strptime(f"{date_str} {time_str} {am_pm}", "%m/%d/%y %I:%M:%S %p")

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
