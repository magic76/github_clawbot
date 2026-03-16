import os
from groq import Groq
from datetime import datetime

def run_lobster():
    # 1. 檢查並讀取 API Key
    api_key = os.getenv("GROQ_API_KEY")
    if not api_key:
        print("錯誤: 找不到 GROQ_API_KEY。請檢查 GitHub Secrets 設定。")
        return

    client = Groq(api_key=api_key)

    # 2. 確保任務檔案存在並讀取內容
    task_file = "tasks.md"
    if not os.path.exists(task_file):
        with open(task_file, "w", encoding="utf-8") as f:
            f.write("請幫我總結今天全球最重要的三則科技新聞。")
        print(f"已建立預設任務檔: {task_file}")

    with open(task_file, "r", encoding="utf-8") as f:
        user_task = f.read().strip()
        if not user_task:
            user_task = "請確認目前系統運作正常，並打個招呼。"

    # 3. 呼叫 Groq API (使用最新的 Llama 模型)
    print(f"正在執行任務: {user_task}")
    try:
        completion = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[
                {
                    "role": "system", 
                    "content": "你是一個住在 GitHub 裡的 AI 代理人（綽號小龍蝦）。請用繁體中文、簡潔有力地完成任務。"
                },
                {"role": "user", "content": user_task}
            ],
        )
        result = completion.choices[0].message.content
    except Exception as e:
        print(f"呼叫 API 時發生錯誤: {e}")
        return

    # 4. 將結果寫入 results.md (加上時間標籤)
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    results_file = "results.md"
    
    # 如果結果檔不存在，先寫入標題
    if not os.path.exists(results_file):
        with open(results_file, "w", encoding="utf-8") as f:
            f.write("# 龍蝦 AI 執行紀錄\n")

    with open(results_file, "a", encoding="utf-8") as f:
        f.write(f"\n---\n")
        f.write(f"### 執行時間: {now}\n")
        f.write(f"{result}\n")
    
    print("任務完成，結果已寫入 results.md")

if __name__ == "__main__":
    run_lobster()
