from aiogram_dialog import Dialog, DialogManager, Window
from aiogram_dialog.widgets.input import ManagedTextInput, TextInput
from aiogram_dialog.widgets.kbd import (Back, Button, Calendar, CalendarConfig,
                                        ScrollingGroup, Select, SwitchTo)
from aiogram_dialog.widgets.text import Const, Format

from bot.src.dialogs.functions.functions import (delete_task_handler,
                                                 view_task_archive)
from bot.src.dialogs.functions.getters import getter_archive, getter_task
from bot.src.fsm.todoFSM import todoFSM

view_archive_window = Window(
    Const("Выполненные задачи"),
    ScrollingGroup(
        Select(
            Format("✅ {item[title]}"),
            items="tasks",
            item_id_getter=lambda task: task["id"],
            id="task_in_category",
            on_click=view_task_archive,
        ),
        id="task_scroll",
        width=1,
        height=5,
    ),
    SwitchTo(Const("🔙 Назад"), id="back_from_archive", state=todoFSM.start),
    getter=getter_archive,
    state=todoFSM.view_archive,
)

view_archive_task_detail_window = Window(
    Format(
        "📌 <b>{task[title]}</b>\n\n"
        "Категория: <b>{task[category][name]}</b>\n\n"
        "Дата создания: <b>{created_at} </b>\n"
        "Дата исполнения: <b>{due_date} {task[due_time]}</b>\n"
        "Описание: {task[description]}\n\n"
        "✅ Выполнено!"
    ),
    Button(Const("🗑 Удалить задачу"), id="delete_task", on_click=delete_task_handler),
    Back(Const("🔙 Назад")),
    getter=getter_task,
    state=todoFSM.view_archive_task_detail,
)
