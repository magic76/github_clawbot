import os
import openai

# 從 GitHub Secrets 讀取 API Key
api_key = os.getenv("OPENAI_API_KEY")
client = openai.OpenAI(api_key=api_key)

def run_task():
    # 讀取任務清單 (例如讀取 Repo 裡的 tasks.md)
    with open("tasks.md", "r") as f:
        task_content = f.read()

    # 叫 AI 執行任務
    response = client.chat.completions.create(
        model="gpt-4o",
        messages=[{"role": "user", "content": f"執行以下任務並回報結果：{task_content}"}]
    )

    # 將結果寫入結果檔
    with open("results.md", "a") as f:
        f.write(f"\n## 執行結果\n{response.choices[0].message.content}\n")

if __name__ == "__main__":
    run_task()
