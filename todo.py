import tkinter as tk
import json
from work import Task
class Task:
    """单个待办任务"""

    def __init__(self, content, completed):
        self.content = content
        self.completed = completed

    def mark_done(self):
        """标记为已完成"""
        # >>> 填空1：把 self.completed 设为 True
        self.completed=True
        pass

    def __str__(self):
        """返回格式化的任务字符串"""
        status = "[v]" if self.completed else "[x]"
        # >>> 填空2：返回格式化的字符串
        return f"{status}:{self.content}"


def show_menu():
    """显示菜单"""
    print("\n===== 待办事项清单 =====")
    print("1. 查看所有任务")
    print("2. 添加任务")
    print("3. 删除任务")
    print("4. 标记完成")
    print("5. 退出")


def show_tasks(tasks):
    """显示所有任务"""
    with open("tasks.json", "r", encoding="utf-8") as f:
        tasks=json.load(f)   
    if not tasks:
        print("暂无任务")
        return
    for i, task in enumerate(tasks, start=1):
        # >>> 填空3：用 task 的 __str__ 方法打印
        print(i,task)



def add_task(tasks):
    """添加任务"""
    content = input("请输入任务内容：")
    # >>> 填空4：创建 Task 对象并加入列表
    s=Task(content, False)
    tasks.append(s)
    print(f"已添加：{content}") 
    
    task_add={[{'content': task.content, 'completed': task.completed} for task in tasks]}    
    with open ('tasks.json','w',encoding='utf-8')as f:
        json.dump(task_add,f,ensure_ascii=False, indent=2,)    
      


def delete_task(tasks):
    """删除任务"""
    with open("tasks.json", "r", encoding="utf-8") as f:
        tasks=json.load(f)
        show_tasks(tasks)
    if not tasks:
        return
    try:
        index = int(input("请输入要删除的任务序号："))
        if 1 <= index <= len(tasks):
            # >>> 填空5：用 pop 删除对应任务
            tasks.pop(index-1)
            with open("tasks.json", "w", encoding="utf-8") as f:
                json.dump(tasks, f, ensure_ascii=False, indent=2)
        else:
            print("序号无效")
    except ValueError:
        print("请输入数字")


def mark_done(tasks):
    """标记任务为已完成"""
    show_tasks(tasks)
    if not tasks:
        return
    try:
        index = int(input("请输入要标记的任务序号："))
        if 1 <= index <= len(tasks):
            # >>> 填空6：调用对应任务的 mark_done 方法
            tasks[index-1].mark_done()
            with open("tasks.json", "w", encoding="utf-8") as f:
                json.dump(tasks, f, ensure_ascii=False, indent=2)
            print("已标记完成！")
        else:
            print("序号无效")
    except ValueError:
        print("请输入数字")
  
def load_tasks():
    try:
        with open ("tasks.json","r",encoding="utf-8")as f:
            tasks = json.load(f)
            f_tasks = []
            for task in tasks:
                f_tasks.append(Task(task.get('content', ''), task.get('completed', False)))
            return f_tasks
        
    except FileNotFoundError:
        print("未找到该文件")
        return []
def main():
    tasks = load_tasks()
    while True:
        show_menu()
        choice = input("请选择（1-5）：")
        if choice == "1":
            show_tasks(tasks)
        elif choice == "2":
            add_task(tasks)
        elif choice == "3":
            delete_task(tasks)
        elif choice == "4":
            mark_done(tasks)
        elif choice == "5":
            # >>> 填空7：退出
            break
        else:
            print("无效选择，请输入 1-5")



    
def clear_list():
    listbox.delete(0, tk.END)
    label_status.config(text="列表已清空")
    
def load_tasks():
    
    try:
        with open("todolist.json", "r", encoding="utf-8") as f:
            alltasks = json.load(f)
            listbox.delete(0, tk.END)
        
        for s in alltasks:
            
            listbox.insert(tk.END, f"s[任务]:s[是否完成]" )

        label_status.config(text=f"加载了 {len(alltasks)} 条记录")
    except FileNotFoundError:
        label_status.config(text="错误信息")
    except json.JSONDecodeError:
        label_status.config(text="JSON 格式错误")

win = tk.Tk()

win.title('任务清单')
win.geometry("420x400")


tk.Label(win, text="任务清单", font=("微软雅黑", 14)).pack()


listbox = tk.Listbox(win, width=40, height=10)
listbox.pack()

tk.Button(win, text="加载任务", command=load_tasks).pack()
tk.Button(win, text="清空", command=clear_list).pack()

label_status = tk.Label(win, text="就绪")
label_status.pack()

win.mainloop()
if __name__ == "__main__":
    main()