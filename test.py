# from data import init_db, add_task
# init_db()
# add_task("写作业",'7月30日','2', "3")
# add_task("跑步",'7月30日','2', "0")
# add_task("买水果",'7月30日','2',)  
# print("添加完成")

# from data import get_all
# for task in get_all():
#     print (f'{task['id']},{task['content']},{task['deadline']},{task['priority']}')

# from data import mark_done, delete
# mark_done('1')
# delete('2')
# from data import get_all
# for task in get_all():
#     print (f'{task['id']},{task['content']},{task['deadline']},{task['completed']}')



from data import init_db, get_all, add_task, mark_done, delete

def show_all():
    tasks = get_all()
    if not tasks:
        print("暂无任务")
        return
    else:
        result=tasks['result']
        for t in result:
            # print(t["result"])
            status = "✓" if t['completed'] else "✗"
            print(f"{t['id']}. [{t['priority']}] [{status}] {t['content']} {t['deadline']} {t['completed']}")

def main():
    init_db()
    while True:
        print("\n===== 待办清单 Plus =====")
        print("1.查看 2.添加 3.标记完成 4.删除 5.退出")
        choice = input("> ")
        if choice == "1":
            show_all()
        elif choice == "2":
            content = input("任务内容：")
            deadline=input('截止日期：')
            importance=input('重要性:')
            priority = input("优先级：") or "1"
            add_task(content, deadline,importance,priority)
            c=add_task(content, deadline,importance,priority)
            if c['res_code']==1:
                print('ok')
            else:
                print('no')
            
        elif choice == "3":
            show_all()
            try:
                tid = int(input("输入要标记完成的任务 ID："))
                mark_done(tid)
                a=mark_done(tid)
                if a['res_code']==1:
                    print("已标记")
                else:
                    print('标记失败')
            except ValueError:
                print("请输入数字")
        elif choice == "4":
            show_all()
            try:
                tid = int(input("输入要删除的任务 ID："))
                delete(tid)
                b=delete(tid)
                if b['res_code']==1:
                    print("已删除")
                else:
                    print('删除失败')
            except ValueError:
                print("请输入数字")
        elif choice == "5":
            break

if __name__ == "__main__":
    main()