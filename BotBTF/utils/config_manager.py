import json
import os

CONFIG_PATH = 'config.json'

def load_config():
    if not os.path.exists(CONFIG_PATH):
        default_config = {
            "prefix": "/",
            "color_purple": "0x9b59b6",
            "color_blue": "0x3498db",
            "special_keywords": ["importante", "ajuda", "btf", "admin"],
            "activity_name": "♨️",
            "welcome_message": "Bem-vindo ao servidor!",
            "xp_min": 5,
            "xp_max": 15
        }
        save_config(default_config)
        return default_config
    
    with open(CONFIG_PATH, 'r', encoding='utf-8') as f:
        return json.load(f)

def save_config(config):
    with open(CONFIG_PATH, 'w', encoding='utf-8') as f:
        json.dump(config, f, indent=4, ensure_ascii=False)
