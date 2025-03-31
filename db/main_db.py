import sqlite3
from config import DB_PATH
from db import queries

def init_db():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    # Удаляем старую таблицу (если она существует), для первоначальной настройки
    cursor.execute("DROP TABLE IF EXISTS tasks")
    
    # Создаем новую таблицу с колонкой in_progress
    cursor.execute(queries.CREATE_TABLE_TASKS)
    conn.commit()
    conn.close()
def get_tasks(filter_type="all"):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    if filter_type == 'completed':
        cursor.execute(queries.SELECT_completed)
    elif filter_type == "incomplete":
        cursor.execute(queries.SELECT_incomplete)
    elif filter_type == "in_progress":
        cursor.execute(queries.SELECT_in_progress)
    else:
        cursor.execute(queries.SELECT_TASKS)

    tasks = cursor.fetchall()
    conn.close()
    return tasks

def add_task_db(task):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute(queries.INSERT_TASK, (task,))
    conn.commit()
    task_id = cursor.lastrowid
    conn.close()
    return task_id

def update_task_db(task_id, new_task=None, completed=None, in_progress=None):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    if new_task is not None:
        cursor.execute("UPDATE tasks SET task = ? WHERE id = ?", (new_task, task_id))
    if completed is not None:
        cursor.execute("UPDATE tasks SET completed = ? WHERE id = ?", (completed, task_id))
    if in_progress is not None:
        cursor.execute("UPDATE tasks SET in_progress = ? WHERE id = ?", (in_progress, task_id))

    conn.commit()
    conn.close()

def delete_task_db(task_id):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute(queries.DELETE_TASK, (task_id,))
    conn.commit()
    conn.close()

def clear_completed_tasks_db():
    """Удаляет все выполненные задачи."""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("DELETE FROM tasks WHERE completed = 1")
    conn.commit()
    conn.close()
