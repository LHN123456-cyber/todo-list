import sqlite3

DB = "todo.db"

def init_db():#创建一个数据库
    with sqlite3.connect(DB) as conn:
        conn.execute("""
        CREATE TABLE IF NOT EXISTS tasks (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            content TEXT NOT NULL,
            deadline DATE NOT NULL,
            importance INTEGER NOT NULL,
            description TEXT NOT NULL,
            priority INTEGER DEFAULT 1,
            status TEXT DEFAULT '未开始'
        )
        """)
  


def get_all():#从数据库中读取数据
    try:
        with sqlite3.connect(DB) as conn:
            conn.row_factory = sqlite3.Row
            rows = conn.execute(
                "SELECT * FROM tasks ORDER BY priority DESC"
                ).fetchall()
            return {
                'res_code':1,
                'result':[dict(r) for r in rows]
                    }
    except Exception:
        return {
            'res_code':1,
            'result':'读取错误'
        }

def add_task(content,deadline,importance,description,priority='1',status='未开始'):#添加数据
    try:
        with sqlite3.connect(DB) as conn:
            conn.execute("INSERT INTO tasks (content,deadline,importance,description,priority,status) VALUES (?, ? , ? , ? ,?,?)",
                    (content,deadline,importance,description,priority,status))
        return {
            'res_code':1,
            'message':'已添加任务'
        }
    except Exception as e:
        print(e)
        return {
            'res_code':2,
            'message':'执行失败'
        }

def mark_done(task_id):#标记数据已完成
    try:
        with sqlite3.connect(DB) as conn:
            conn.execute("UPDATE tasks SET completed = 1 WHERE id = ?", (task_id,))
        return {
            'res_code':1,
            'message': '成功执行'   
                }
    except Exception:
        return {'res_code':2}
        



def delete(task_id):#删除某一任务
    try:
        with sqlite3.connect(DB) as conn:
            conn.execute("DELETE FROM tasks WHERE id = ?", (task_id,))
        return {
            'res_code':1,
            'message':'成功执行'   
            }
    except Exception:
        return {'res_code':2}
    
    
def fix(content,deadline,importance,description,priority,status,t_id):
    try:
        with sqlite3.connect(DB) as conn:
            conn.execute("""
            UPDATE tasks
            SET
                content = '?',
                status = '?',
                priority = '?',
                importance = '?',
                deadline = '?',
                description = '?',
            WHERE t_id = ?
            """,
            (content,status,priority,importance,deadline,description,t_id)
            )
            return {
                    'res_code':1,
                    'message':'成功执行'   
                     }
    except Exception:
          return {'res_code':2}
        
    
                             
    
