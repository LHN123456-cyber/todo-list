import data
from ui import TodoApp
import tkinter as tk

    
from api import judge_priority

# def ai_cb():
#     message = data.get_all()
#     message2 = message['result']
#     for x_content in message2:
#         if not x_content: TodoApp.title_label.config(text="请先输入任务内容"); return
#         TodoApp.title_label.config(text="AI 评估中...")
#         root.update()
#         priority = judge_priority(x_content)
        
#         TodoApp.title_label.config(text=f"AI 判断：{priority}优先级")
        
        
    
if __name__ == "__main__":
    data.init_db()
    # TodoApp.ai_cb(self)
    root = tk.Tk()
    app = TodoApp(root)
    root.mainloop()