import os
from groq import Groq

client = Groq(api_key=os.getenv("GROQ_API_KEY"))

def run_task():
    # 讀取任務
    with open("tasks.md", "r", encoding="utf-8") as f:
        task = f.read()

    # 呼叫 Groq
    completion = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[
            {"role": "system", "content": "你是一個有效率的 AI 代理人。"},
            {"role": "user", "content": task}
        ],
    )

    # 儲存結果
    with open("results.md", "a", encoding="utf-8") as f:
        f.write(f"\n\n### 執行結果\n{completion.choices[0].message.content}\n")

if __name__ == "__main__":
    run_task()
