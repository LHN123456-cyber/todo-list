import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
import data
from api import judge_priority

class TodoApp:
    def __init__(self, root):
        self.root = root
        self.root.title("待办清单")
        self.root.geometry("900x600")

        main_pane = ttk.PanedWindow(root, orient=tk.HORIZONTAL)
        main_pane.pack(fill=tk.BOTH, expand=True)

        left_frame = ttk.Frame(main_pane, width=300)
        main_pane.add(left_frame, weight=1)  # weight 控制拉伸比例

        toolbar = ttk.Frame(left_frame)
        toolbar.pack(fill=tk.X, pady=5)

        btn_add = ttk.Button(toolbar, text="新增任务",command=self.show_add)
        btn_add.pack(side=tk.LEFT, padx=2)
        btn_delete = ttk.Button(toolbar, text="删除任务",command=self.show_del)
        btn_delete.pack(side=tk.LEFT, padx=2)
        btn_clear = ttk.Button(toolbar, text="AI 评估",command=self.ai_cb)
        btn_clear.pack(side=tk.LEFT, padx=2)
        # 为了美观，右侧加一个弹性占位
        ttk.Label(toolbar, text="").pack(side=tk.LEFT, fill=tk.X, expand=True)

        list_frame = ttk.Frame(left_frame)
        list_frame.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)

        # 创建 Treeview 并添加滚动条
        columns = ("id", "content", "completed", "priority")
        self.tree = ttk.Treeview(
            list_frame, columns=columns, show="headings", height=15
        )
        self.tree.heading("id", text="ID")
        self.tree.heading("content", text="标题")
        self.tree.heading("completed", text="状态")
        self.tree.heading("priority", text="优先级")
        self.tree.column("id", width=40, anchor=tk.CENTER)
        self.tree.column("content", width=120)
        self.tree.column("completed", width=80, anchor=tk.CENTER)
        self.tree.column("priority", width=70, anchor=tk.CENTER)

        vsb = ttk.Scrollbar(list_frame, orient=tk.VERTICAL, command=self.tree.yview)
        self.tree.configure(yscrollcommand=vsb.set)  # 设置一个竖直方向的滚动条
        self.tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        vsb.pack(side=tk.RIGHT, fill=tk.Y)

        self.tree.bind("<<TreeviewSelect>>", self.on_tree_select)

        # ---------- 右侧区域 ----------
        right_frame = ttk.Frame(main_pane)
        main_pane.add(right_frame, weight=2)  # 右侧占据更多空间

        # 右侧上部：标题 + 操作按钮（水平布局）
        top_right = ttk.Frame(right_frame)
        top_right.pack(fill=tk.X, pady=5, padx=5)

        # 标题（左侧）
        self.title_label = ttk.Label(
            top_right, text="任务详情", font=("Arial", 14, "bold")
        )  # 字体
        self.title_label.pack(side=tk.LEFT)

        # 右侧按钮组（靠右）
        btn_frame = ttk.Frame(top_right)
        btn_frame.pack(side=tk.RIGHT)
        self.btn_save = ttk.Button(btn_frame, text="保存修改", command=self.save_task)
        self.btn_save.pack(side=tk.LEFT, padx=2)
        self.btn_add = ttk.Button(btn_frame, text="确认新增", command=self.do_add)
        self.btn_delete = ttk.Button(btn_frame, text="确认删除", command=self.do_del)

        # 右侧下部：详情表单（使用 grid 布局）
        
        detail_frame = ttk.LabelFrame(
            right_frame, text="编辑任务", padding=10
        )  # 划分了一个区域
        detail_frame.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)

        ttk.Label(detail_frame, text="任务ID:").grid(
            row=0, column=0, sticky=tk.W, pady=5
        )  # 行列布局
        self.entry_id = ttk.Entry(detail_frame, state="readonly", width=30)
        self.entry_id.grid(
            row=0, column=1, sticky=tk.W, padx=5, pady=5
        )  # 创建输入框单只读不可改

        # 行1：标题
        ttk.Label(detail_frame, text="标题:").grid(row=1, column=0, sticky=tk.W, pady=5)
        self.entry_title = ttk.Entry(detail_frame, width=30)
        self.entry_title.grid(row=1, column=1, sticky=tk.W, padx=5, pady=5)

        # 行2：状态（下拉选择）
        ttk.Label(detail_frame, text="状态:").grid(row=2, column=0, sticky=tk.W, pady=5)
        self.combo_status = ttk.Combobox(
            detail_frame, values=["未开始","进行中", "已完成"], state="readonly", width=28
        )
        self.combo_status.grid(row=2, column=1, sticky=tk.W, padx=5, pady=5)

        # 行3：优先级（下拉选择）
        ttk.Label(detail_frame, text="优先级:").grid(
            row=3, column=0, sticky=tk.W, pady=5
        )
        self.combo_priority = ttk.Combobox(
            detail_frame, values=["低", "中", "高"], state="readonly", width=28
        )
        self.combo_priority.grid(row=3, column=1, sticky=tk.W, padx=5, pady=5)
        
        
        ttk.Label(detail_frame, text="重要性:").grid(
            row=4, column=0, sticky=tk.W, pady=5
        )
        self.combo_importance = ttk.Combobox(
            detail_frame, values=['1','2','3','4','5'], state="readonly", width=28
        )
        self.combo_importance.grid(row=4, column=1, sticky=tk.W, padx=5, pady=5)

        # 行4：截止日期（简单输入框，实际可用DateEntry等）
        ttk.Label(detail_frame, text="截止日期:").grid(
            row=5, column=0, sticky=tk.W, pady=5
        )
        self.entry_deadline = ttk.Entry(detail_frame, width=30)
        self.entry_deadline.grid(row=5, column=1, sticky=tk.W, padx=5, pady=5)

        # 行5：描述（多行文本框）
        ttk.Label(detail_frame, text="描述:").grid(
            row=6, column=0, sticky=tk.NW, pady=5
        )
        self.text_desc = tk.Text(detail_frame, width=30, height=6)
        self.text_desc.grid(row=6, column=1, sticky=tk.W, padx=5, pady=5)

        # 填充一些示例数据
        self.load_db_data()

        # 清除当前选中的高亮，显示空白详情
        self.clear_details()

    def load_db_data(self):
        a = data.get_all()
        if a["res_code"] == 1:
            for t in a['result']:
                self.tree.insert("", tk.END, values=(t['id'],t['content'],t['status'],t['priority']))
        else:
            messagebox.showerror("错误","请检查相应设置")

    def on_tree_select(self, event):
        """当在列表中选择一项时，在右侧显示其详情"""
        self.title_label.config(text='任务详情')  
        self.btn_add.pack_forget()
        self.btn_save.pack(side=tk.LEFT, padx=2)
        selected = self.tree.selection()
        if not selected:
            return
        # 获取选中行的值
        values = self.tree.item(selected[0], "values")
        if values:
            res = data.get_all()
            if res["res_code"] == 1:
                for t in res['result']:
                    self.entry_id.config(state="normal")
                    self.entry_id.delete(0, tk.END)
                    self.entry_id.insert(0, values[0])
                    self.entry_id.config(state="readonly")

                    self.entry_title.delete(0, tk.END)
                    self.entry_title.insert(0, values[1])

                    self.combo_status.set(values[2])
                    self.combo_priority.set(values[3])
                    
                    self.combo_importance.set(t['importance'])

                    # 描述、截止日期这里没有数据，可留空或设置默认
                    self.text_desc.delete("1.0", tk.END)
                    self.text_desc.insert("1.0", t['description'])  # 做替换

                    self.entry_deadline.delete(0, tk.END)
                    self.entry_deadline.insert(0, t['deadline'])
            else:
                messagebox.showerror("错误","请检查相应设置")

    def save_task(self):
        """保存修改（示例）"""
        # 获取当前选中的任务ID
        selected = self.tree.selection()
        if not selected:
            print("未选中任何任务")
            return
        # 这里仅演示打印新值，实际应更新数据库或列表
        new_values = (
            self.entry_id.get(),
            self.entry_title.get(),
            self.combo_status.get(),
            self.combo_priority.get(),
            self.combo_importance.get(),
            self.text_desc.get('1.0',tk.END),
            self.entry_deadline.get()
        )
        print(f"保存任务 {new_values}")
        # 更新Treeview中对应的行
        self.tree.item(selected[0], values=new_values)

    def clear_details(self):
        """清空右侧详情区域"""
        self.entry_id.config(state="normal")
        self.entry_id.delete(0, tk.END)
        self.entry_id.config(state="readonly")
        self.entry_title.delete(0, tk.END)
        self.combo_status.set("")
        self.combo_priority.set("")
        self.entry_deadline.delete(0, tk.END)
        self.text_desc.delete("1.0", tk.END)

    def refresh_tree(self):
        for item in self.tree.get_children():
            self.tree.delete(item)
        self.load_db_data()

    def show_add(self):
        self.title_label.config(text='新增任务')  
        self.btn_save.pack_forget()
        self.btn_add.pack(side=tk.LEFT, padx=2)
        
    def show_del(self):
        self.title_label.config(text='删除任务')  
        self.btn_save.pack_forget()
        self.btn_delete.pack(side=tk.LEFT, padx=2)
        
        
    def do_add(self):
        res = data.add_task(
            self.entry_title.get(),
            self.entry_deadline.get(),
            self.combo_importance.get(),
            self.text_desc.get("1.0", tk.END),
            self.combo_priority.get(),
            self.combo_status.get()   
        )
        if res['res_code']==1:
            messagebox.showinfo('提示','添加成功')
            self.refresh_tree()
      

    def do_del(self):
        sel = self.tree.selection()
        if not sel: self.title_label.config(text="请先选中一条任务", ); return
        self.btn_save.pack_forget()
        self.btn_delete.pack(side=tk.LEFT, padx=2)
        data.delete(self.tree.item(sel[0])["values"][0])
        res = data.delete(self.entry_id.get())
        if res['res_code']==1:
            messagebox.showinfo('提示','删除成功')
            self.refresh_tree()
            
            
    def ai_cb(self):
        a = data.get_all()
        res = a['result']
        for content in res:
            if not content: self.title_label.config(text="请先输入任务内容"); return
            self.title_label.config(text="AI 评估中...")
            self.root.update()
            priority = judge_priority(content)
            self.title_label.config(text=f"AI 判断：{priority}优先级")


if __name__ == "__main__":
    data.init_db()
    root = tk.Tk()
    app = TodoApp(root)
    root.mainloop()


