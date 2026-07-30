import sqlite3

DB = "todo.db"

def init_db():
    with sqlite3.connect(DB) as conn:
        conn.execute("""
        CREATE TABLE IF NOT EXISTS tasks (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            content TEXT NOT NULL,
            deadline DATE NOT NULL,
            importance INTEGER NOT NULL,
            priority INTEGER DEFAULT 1,
            completed INTEGER DEFAULT 0
        )
        """)
    return None


def get_all():
    with sqlite3.connect(DB) as conn:
        conn.row_factory = sqlite3.Row
        rows = conn.execute(
            "SELECT * FROM tasks ORDER BY priority DESC"
            ).fetchall()
        return [dict(r) for r in rows]

def add_task(content,deadline,importance,priority='1',completed='0'):
    with sqlite3.connect(DB) as conn:
        conn.execute("INSERT INTO tasks (content,deadline,importance,priority,completed) VALUES (?, ? , ? , ? ,?)",
                    (content,deadline,importance,priority,completed))


def mark_done(task_id):
    with sqlite3.connect(DB) as conn:
        conn.execute("UPDATE tasks SET completed = 1 WHERE id = ?", (task_id,))



def delete(task_id):
    with sqlite3.connect(DB) as conn:
        conn.execute("DELETE FROM tasks WHERE id = ?", (task_id,))
