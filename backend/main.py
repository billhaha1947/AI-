import os
import time
import requests
import torch
from fastapi import FastAPI, HTTPException, Header
from pydantic import BaseModel
from transformers import AutoTokenizer, AutoModelForCausalLM, BitsAndBytesConfig
from news_fetcher import fetch_news_from_feeds
from utils import save_chat_log, load_chat_logs

app = FastAPI(title="Rồng Máy AI Online")

# --- Load model 4-bit để nhanh và ít tốn RAM ---
MODEL_NAME = "google/gemma-2b-it"
tokenizer = AutoTokenizer.from_pretrained(MODEL_NAME)

bnb_config = BitsAndBytesConfig(
    load_in_4bit=True,
    bnb_4bit_compute_dtype=torch.float16,
)

model = AutoModelForCausalLM.from_pretrained(MODEL_NAME, quantization_config=bnb_config)
model.eval()

# Admin token (sẽ đổi được trong Render dashboard)
ADMIN_TOKEN = os.environ.get("ADMIN_TOKEN", "tao-la-admin")

class ChatRequest(BaseModel):
    message: str

@app.post("/chat")
async def chat(req: ChatRequest):
    inp = tokenizer(req.message, return_tensors="pt")
    with torch.no_grad():
        out = model.generate(**inp, max_new_tokens=80, do_sample=True, top_p=0.9)
    reply = tokenizer.decode(out[0], skip_special_tokens=True)

    save_chat_log(req.message, reply)
    return {"reply": reply}

@app.get("/news")
async def news(limit: int = 10):
    try:
        items = fetch_news_from_feeds(limit)
        return {"items": items}
    except Exception as e:
        raise HTTPException(500, str(e))

@app.get("/admin/logs")
async def admin_logs(x_admin_token: str = Header(None)):
    if x_admin_token != ADMIN_TOKEN:
        raise HTTPException(401, "Sai admin token rồi")
    return {"logs": load_chat_logs()}

@app.get("/health")
async def health():
    return {"status": "ok", "time": int(time.time())}
