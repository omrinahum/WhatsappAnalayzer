"""
Hebrew fixer for data, dictionaries, lables using Bidi Algorithm
"""

import arabic_reshaper
from bidi.algorithm import get_display
import re

def fix_hebrew(text: str) -> str:
    """Fix Hebrew text for display in Plotly or Matplotlib.
    Reorders text using arabic_reshaper and python-bidi."""
    # Check if the text contains Hebrew characters, if so, reshape and reorder it
    if isinstance(text, str) and re.search(r'[\u0590-\u05FF]', text):
        reshaped = arabic_reshaper.reshape(text)
        return get_display(reshaped)
    return text

def fix_labels(labels: list[str]) -> list[str]:
    return [fix_hebrew(label) for label in labels]

def fix_dict_keys(d: dict) -> dict:
    return {fix_hebrew(k): v for k, v in d.items()}
