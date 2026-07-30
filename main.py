from data import init_db, get_all, add_task, mark_done, delete
def main():
    init_db()
    print("数据库初始化完成")
    print("当前任务：", get_all())

if __name__ == "__main__":
    main()