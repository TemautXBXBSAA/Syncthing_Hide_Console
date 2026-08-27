import json
import os
def read_config(default_config = {}):
    if not os.path.exists("config.json"):
        write_config(default_config)
        return default_config
    with open("config.json", "r", encoding="utf-8") as f:
        return json.load(f)

def write_config(config):
    with open("config.json", "w", encoding="utf-8") as f:
        json.dump(config, f, ensure_ascii=False, indent=4)