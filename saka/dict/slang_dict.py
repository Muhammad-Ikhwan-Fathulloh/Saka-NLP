import json
import os
from typing import Dict

def get_slang_dict() -> Dict[str, str]:
    """
    Returns a dictionary of common Indonesian slang words mapped to standard words.
    """
    current_dir = os.path.dirname(__file__)
    json_path = os.path.join(current_dir, 'slang.json')
    try:
        with open(json_path, 'r', encoding='utf-8') as f:
            return json.load(f)
    except FileNotFoundError:
        return {}
