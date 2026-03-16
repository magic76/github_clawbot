import os
from groq import Groq
from datetime import datetime
from duckduckgo_search import DDGS

def run_lobster():
    api_key = os.getenv("GROQ_API_KEY")
    if not api_key:
        print("錯誤: 找不到 GROQ_API_KEY")
        return

    client = Groq(api_key=api_key)

    # 1. 讀取任務
    task_file = "tasks.md"
    if not os.path.exists(task_file):
        with open(task_file, "w", encoding="utf-8") as f:
            f.write("查詢今天新北市土城區的天氣與三則科技新聞。")

    with open(task_file, "r", encoding="utf-8") as f:
        user_task = f.read().strip()

    # 2. 自動執行搜尋 (搜尋與任務相關的即時資訊)
    print(f"正在為任務進行聯網搜尋: {user_task}")
    search_results = ""
    try:
        with DDGS() as ddgs:
            # 抓取前 5 筆相關搜尋結果
            results = [r for r in ddgs.text(user_task, max_results=5)]
            search_results = "\n".join([f"標題: {r['title']}\n摘要: {r['body']}" for r in results])
    except Exception as e:
        print(f"搜尋失敗: {e}")
        search_results = "無法取得即時資訊。"

    # 3. 呼叫 Groq 並餵入搜尋到的資料
    print("正在彙整資料並產出回報...")
    try:
        prompt = f"""
        使用者任務: {user_task}
        以下是從網路上搜尋到的即時資訊:
        {search_results}
        
        請根據以上資訊，精簡地回答使用者的任務。
        """
        
        completion = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[
                {"role": "system", "content": "你是一個具備連網能力的 AI 代理人（小龍蝦）。請用繁體中文回答。"},
                {"role": "user", "content": prompt}
            ],
        )
        result = completion.choices[0].message.content
    except Exception as e:
        print(f"AI 產出失敗: {e}")
        return

    # 4. 寫回結果
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    results_file = "results.md"
    with open(results_file, "a", encoding="utf-8") as f:
        f.write(f"\n---\n### 執行時間: {now} (連網模式)\n{result}\n")
    
    print("連網任務完成！")

if __name__ == "__main__":
    run_lobster()
