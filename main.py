import flet as ft
from db import main_db
import random

def main(page: ft.Page):
    page.title = 'Todo List'
    page.theme_mode = ft.ThemeMode.DARK
    page.window_maximized = True 

    task_list = ft.Column(spacing=10)
    filter_type = "all"
    warning_text = ft.Text("", color=ft.colors.RED)

    def load_tasks():
        task_list.controls.clear()
        for task_id, task_text, completed in main_db.get_tasks(filter_type):
            task_list.controls.append(create_task_row(task_id, task_text, completed))
        page.update()

    def create_task_row(task_id, task_text, completed):
        task_field = ft.TextField(value=task_text, expand=True, dense=True, read_only=True)
        task_checkbox = ft.Checkbox(
            value=bool(completed), 
            on_change=lambda e: toggle_task(task_id, e.control.value)
        )

        def enable_edit(e):
            task_field.read_only = False
            page.update()

        def save_edit(e):
            main_db.update_task_db(task_id, task_field.value)
            task_field.read_only = True
            page.update()

        return ft.Row([
            task_checkbox,
            task_field,
            ft.IconButton(ft.icons.EDIT, icon_color=ft.colors.YELLOW_400, on_click=enable_edit),
            ft.IconButton(ft.icons.SAVE, icon_color=ft.colors.GREEN_400, on_click=save_edit),
            ft.IconButton(ft.icons.DELETE, icon_color=ft.colors.RED_400, on_click=lambda e: delete_task(task_id))
        ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN)
    
    def on_text_change(e):
        if len(task_input.value) > 100:
            warning_text.value = "Максимальная длина задачи — 100 символов!"
        else:
            warning_text.value = ""
        page.update()

    def add_task(e):
        if task_input.value.strip():
            task_id = main_db.add_task_db(task_input.value)
            task_list.controls.append(create_task_row(task_id, task_input.value))
            task_input.value = ""
            warning_text.value = ""
        page.update()

    def toggle_task(task_id, is_completed):
        main_db.update_task_db(task_id, completed=int(is_completed))
        load_tasks()

    def delete_task(task_id):
        main_db.delete_task_db(task_id)
        load_tasks()

    def clear_completed_tasks(e):
        main_db.clear_completed_tasks_db()  # Метод для очистки выполненных задач в базе
        load_tasks()
    
    def set_filter(filter_value):
        nonlocal filter_type 
        filter_type = filter_value
        load_tasks()
    
    def change_background_color(e):
        colors = [ft.colors.BLUE, ft.colors.RED, ft.colors.GREEN, ft.colors.YELLOW, ft.colors.PURPLE]
        page.bgcolor = random.choice(colors)
        page.update()
    
    task_input = ft.TextField(
        hint_text='Добавьте задачу', 
        expand=True, 
        dense=True, 
        max_length=100,  # Ограничение на 100 символов
        on_change=on_text_change,  # обработчик изменения текста
        on_submit=add_task
    )
    add_button = ft.ElevatedButton("Добавить", on_click=add_task, icon=ft.icons.ADD)
    color_button = ft.ElevatedButton("Сменить фон", on_click=change_background_color)
    clear_button = ft.ElevatedButton("Очистить выполненные", on_click=clear_completed_tasks)  # Кнопка для очистки выполненных

    filter_button = ft.Row([
        ft.ElevatedButton("Все", on_click=lambda e: set_filter("all")),
        ft.ElevatedButton("Выполненные", on_click=lambda e: set_filter("completed")),
        ft.ElevatedButton("Невыполненные", on_click=lambda e: set_filter("incomplete"))
    ], alignment=ft.MainAxisAlignment.CENTER)

    content = ft.Container(
        content=ft.Column([
            ft.Row([task_input, add_button, color_button, clear_button], alignment=ft.MainAxisAlignment.SPACE_BETWEEN),
            warning_text,
            filter_button,
            task_list
        ], alignment=ft.MainAxisAlignment.CENTER), 
        padding=20,
        alignment=ft.alignment.center
    )

    page.add(content)
    load_tasks()

if __name__ == '__main__':
    main_db.init_db()
    ft.app(target=main)
