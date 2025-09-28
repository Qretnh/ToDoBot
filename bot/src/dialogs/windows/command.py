from aiogram_dialog import Window
from aiogram_dialog.widgets.kbd import SwitchTo
from aiogram_dialog.widgets.text import Const

from bot.src.fsm.todoFSM import todoFSM

commands_window = Window(
    Const(
        "Ваш персональный TO-DO лист\n\n"
        "<i>📖 Просмотреть все задачи</i> - \n"
        "Нажмите, чтобы просмотреть полный список задач\n\n"
        "<i>📋 Задачи по категориям</i> - \n"
        "Чтобы ➕ открыть задачи конкретной категории ИЛИ удалить/завершить✅ задачу\n\n"
        "<i>✏️ Изменить категории</i> - \n"
        "Удаление категорий\n\n"
        "<i>➕ Добавить задачу</i> - \n"
        "Создание новой задачи\n\n"
        "<i>📁 Архив</i> - \n"
        "Просмотреть завершенные задачи"
    ),
    SwitchTo(Const("➕ Добавить задачу"), id="add_task", state=todoFSM.add_task),
    SwitchTo(
        Const("📖 Просмотреть все задачи"), id="open_tasks", state=todoFSM.my_tasks
    ),
    SwitchTo(
        Const("📋 Управление задачами"),
        id="tasks_by_category",
        state=todoFSM.tasks_by_category,
    ),
    SwitchTo(
        Const("✏️ Изменить категории"),
        id="change_category",
        state=todoFSM.manage_category,
    ),
    SwitchTo(Const("📁 Архив"), id="archive", state=todoFSM.view_archive),
    state=todoFSM.start,
)
