CREATE_TABLE_TASKS = """
    CREATE TABLE IF NOT EXISTS tasks (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        task TEXT NOT NULL,
        completed INTEGER DEFAULT 0,
        in_progress INTEGER DEFAULT 0  -- Добавили поле для статуса "В работе"
    )
"""

SELECT_TASKS = "SELECT id, task, completed, in_progress FROM tasks"

INSERT_TASK = "INSERT INTO tasks (task) VALUES (?)"

UPDATE_TASK = "UPDATE tasks SET task = ? WHERE id = ?"

UPDATE_TASK_IN_PROGRESS = "UPDATE tasks SET in_progress = ? WHERE id = ?"

DELETE_TASK = "DELETE FROM tasks WHERE id = ?"

SELECT_completed = 'SELECT id, task, completed, in_progress FROM tasks WHERE completed = 1'

SELECT_incomplete = 'SELECT id, task, completed, in_progress FROM tasks WHERE completed = 0'

SELECT_in_progress = 'SELECT id, task, completed, in_progress FROM tasks WHERE in_progress = 1'
