import os
import requests
from groq import Groq
from datetime import datetime
from duckduckgo_search import DDGS

def send_to_telegram(text):
    token = os.getenv("TELEGRAM_BOT_TOKEN")
    chat_id = os.getenv("TELEGRAM_CHAT_ID")
    if not token or not chat_id:
        print("跳過 TG 發送：未設定 Secret")
        return
    
    # 確保訊息不超過 TG 上限 (4096 字符)
    safe_text = (text[:4000] + '...') if len(text) > 4000 else text
    url = f"https://api.telegram.org/bot{token}/sendMessage"
    payload = {"chat_id": chat_id, "text": safe_text}
    
    try:
        requests.post(url, json=payload, timeout=10)
        print("✅ TG 訊息已發送")
    except Exception as e:
        print(f"❌ TG 發送失敗: {e}")

def run_lobster():
    api_key = os.getenv("GROQ_API_KEY")
    client = Groq(api_key=api_key)

    # 1. 讀取任務
    with open("tasks.md", "r", encoding="utf-8") as f:
        user_task = f.read().strip()

    # 2. 聯網搜尋
    print(f"🔍 搜尋中: {user_task}")
    search_results = ""
    try:
        with DDGS() as ddgs:
            results = [r for r in ddgs.text(user_task, max_results=5)]
            search_results = "\n".join([f"- {r['title']}: {r['body']}" for r in results])
    except:
        search_results = "搜尋失敗，僅依賴 AI 現有知識。"

    # 3. AI 總結
    prompt = f"任務：{user_task}\n參考資料：\n{search_results}\n\n請精簡回答。"
    completion = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[
            {"role": "system", "content": "你是一個住在 GitHub 的 AI 代理人「小龍蝦」。"},
            {"role": "user", "content": prompt}
        ],
    )
    result = completion.choices[0].message.content

    # 4. 存檔與 TG 回報
    now = datetime.now().strftime("%Y-%m-%d %H:%M")
    report = f"🦞 **龍蝦回報 ({now})**\n\n{result}"
    
    # 寫入 results.md
    with open("results.md", "a", encoding="utf-8") as f:
        f.write(f"\n---\n{report}\n")
    
    # 發送到 Telegram
    send_to_telegram(report)

if __name__ == "__main__":
    run_lobster()
