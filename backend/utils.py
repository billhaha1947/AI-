import json
import os
from pathlib import Path
import time

DATA_DIR = Path("/tmp/project_data")
DATA_DIR.mkdir(parents=True, exist_ok=True)
CHAT_LOG_FILE = DATA_DIR / "chat_logs.jsonl"

def save_chat_log(q, a):
    entry = {"question": q, "answer": a, "time": int(time.time.time())}
    with open(CHAT_LOG_FILE, "a", encoding="utf-8") as f:
        f.write(json.dumps(entry, ensure_ascii=False) + "\n")

def load_chat_logs(limit=200):
    if not CHAT_LOG_FILE.exists():
        return []
    logs = []
    with open(CHAT_LOG_FILE, "r", encoding="utf-8") as f:
        for line in f:
            try:
                logs.append(json.loads(line))
            except:
                continue
    return list(reversed(logs))[:limit]
