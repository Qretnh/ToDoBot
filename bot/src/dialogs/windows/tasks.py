import datetime

from aiogram_dialog import Dialog, DialogManager, Window
from aiogram_dialog.widgets.input import TextInput
from aiogram_dialog.widgets.kbd import (Back, Button, Calendar, CalendarConfig,
                                        ScrollingGroup, Select, SwitchTo)
from aiogram_dialog.widgets.text import Const, Format

from bot.src.dialogs.functions.functions import (complete_task_handler,
                                                 delete_task_handler,
                                                 on_add_task,
                                                 on_category_chosen,
                                                 on_category_select_for_tasks,
                                                 on_confirm,
                                                 on_create_category,
                                                 on_date_selected,
                                                 on_description_entered,
                                                 on_description_updated,
                                                 on_no_description,
                                                 on_skip_time, on_time_entered,
                                                 save_title, view_task_detail)
from bot.src.dialogs.functions.getters import (getter_categories,
                                               getter_confirm_task,
                                               getter_selected_category_tasks,
                                               getter_task,
                                               getter_tasks_by_category,
                                               getter_tasks_data)
from bot.src.fsm.todoFSM import todoFSM

my_tasks_window = Window(
    Format("📝 <b>Актуальные задачи</b>:\n\n{tasks_text}\n"),
    Const("Чтобы добавить новую задачу — нажмите кнопку ниже 👇"),
    Button(Const("➕ Добавить задачу"), id="add_task", on_click=on_add_task),
    SwitchTo(Const("🔙 Назад"), id="confirm_task_", state=todoFSM.start),
    state=todoFSM.my_tasks,
    getter=getter_tasks_data,
)

add_tasks_window = Window(
    Const(
        "✍️ <b>Введите название новой задачи</b>:\n\n"
        'Например: "Сходить в спортзал" или "Закончить отчёт" 🗒'
    ),
    TextInput(id="input_title", type_factory=lambda text: text, on_success=save_title),
    Back(Const("🔙 Назад")),
    state=todoFSM.add_task,
)

pick_date_window = Window(
    Const(
        "📅 Выберите дату выполнения задачи (Нажмите на подходящую дату в календаре):"
    ),
    Calendar(
        id="calendar",
        config=CalendarConfig(min_date=datetime.date.today()),
        on_click=on_date_selected,
    ),
    Back(Const("🔙 Назад")),
    state=todoFSM.pick_date,
)
pick_category_window = Window(
    Const(
        "🗂 Выберите категорию из списка, либо введите название новой категории (она создастся автоматически):"
    ),
    Select(
        Format("{item[name]}"),
        items="categories",
        item_id_getter=lambda c: str(c["id"]),
        id="category_select",
        on_click=on_category_chosen,
    ),
    TextInput(
        id="new_category_input",
        type_factory=lambda text: text,
        on_success=on_create_category,
    ),
    Back(Const("🔙 Назад")),
    state=todoFSM.pick_category,
    getter=getter_categories,
)

input_description_window = Window(
    Const(
        "✍️ Введите описание задачи или нажмите кнопку 'Без описания', если оно не требуется"
    ),
    TextInput(
        id="input_description",
        type_factory=lambda text: text,
        on_success=on_description_updated,
    ),
    Button(Const("Без описания"), id="no_desc", on_click=on_no_description),
    Back(Const("🔙 Назад")),
    state=todoFSM.input_description,
)
input_time_window = Window(
    Const(
        "⏰ Введите время выполнения задачи в формате HH:MM (пример - 09:30)\n\n"
        "Или нажмите 'Пропустить' — по умолчанию задача будет на 18:00"
    ),
    TextInput(
        id="input_time", type_factory=lambda text: text, on_success=on_time_entered
    ),
    Button(Const("Пропустить"), id="skip_time", on_click=on_skip_time),
    Back(Const("🔙 Назад")),
    state=todoFSM.input_time,
)
confirm_task_window = Window(
    Format(
        "✅ <b>Подтвердите добавление задачи</b>:\n\n"
        "🗂 <b>Задача:</b> {title}\n"
        "📅 <b>Выполнить до:</b> {due_date} {due_time}\n"
        "📝 <b>Описание:</b> {description}\n\n"
        "Если всё верно — жмите ✅"
    ),
    Button(Format("✅ Подтвердить"), id="confirm", on_click=on_confirm),
    Back(Const("🔙 Назад")),
    getter=getter_confirm_task,
    state=todoFSM.confirm_task,
)
tasks_by_category_window = Window(
    Const(
        "📂 Выберите категорию для просмотра задач\n\n"
        "(Отображаются только категории, в которых есть задачи)"
    ),
    ScrollingGroup(
        Select(
            Format("{item}"),
            items="grouped_tasks",
            item_id_getter=lambda item: item,
            id="category_choice",
            on_click=on_category_select_for_tasks,
        ),
        id="categories_scroll",
        width=1,
        height=5,
    ),
    SwitchTo(Const("🔙 Назад"), id="back_from_manage_categories", state=todoFSM.start),
    getter=getter_tasks_by_category,
    state=todoFSM.tasks_by_category,
)
task_list_by_category_window = Window(
    Format("📂 <b>Задачи в категории {category}</b>\n\n"),
    ScrollingGroup(
        Select(
            Format("{item[title]}"),
            items="TODO",
            item_id_getter=lambda task: task["id"],
            id="task_in_category",
            on_click=view_task_detail,
        ),
        id="task_scroll",
        width=1,
        height=5,
    ),
    Back(Const("🔙 Назад")),
    getter=getter_selected_category_tasks,
    state=todoFSM.task_list_by_category,
)
task_detail_window = Window(
    Format(
        "📌 <b>{task[title]}</b>\n\n"
        "Категория: <b>{task[category][name]}</b>\n\n"
        "Дата создания: <b>{created_at} </b>\n"
        "Дата исполнения: <b>{due_date} {task[due_time]}</b>\n"
        "Описание: {task[description]}"
    ),
    Button(Const("✅ Завершить задачу"), id="complete", on_click=complete_task_handler),
    Button(Const("🗑 Удалить задачу"), id="delete_task", on_click=delete_task_handler),
    SwitchTo(
        Const("✍️ Обновить описание"),
        id="update_description",
        state=todoFSM.update_task_description,
    ),
    Back(Const("🔙 Назад")),
    getter=getter_task,
    state=todoFSM.task_detail,
)
update_task_description_window = Window(
    Const("Введите новое описание задачи"),
    TextInput(
        id="input_description",
        type_factory=lambda text: text,
        on_success=on_description_entered,
    ),
    state=todoFSM.update_task_description,
)
