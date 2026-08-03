import os, requests

API_KEY = os.environ.get("DEEPSEEK_API_KEY", 'apikey')
API_URL = "https://api.deepseek.com/chat/completions"

def judge_priority(task_content):
    prompt = f"""你是一个任务管理助手。根据任务内容判断优先级。
规则：紧急/deadline/考试→高，重要/本周/项目→中，日常不紧急→低。只输出一个字：高、中 或 低。
任务：{task_content}"""

    headers = {"Authorization": f"Bearer {API_KEY}", "Content-Type": "application/json"}
    data = {"model": "deepseek-v4-flash", "messages": [{"role": "user", "content": prompt}],
            "temperature": 0.1, "max_tokens": 5, "stream": False}
    try:
        response = requests.post(API_URL, headers=headers, json=data, timeout=15)
        result = response.json()
        priority = result["choices"][0]["message"]["content"].strip()
        return priority if priority in ("高", "中", "低") else "中"
    except Exception as e:
        print(f"AI 判断失败：{e}")
        return "失败"
''''''