from aiogram_dialog import Dialog, DialogManager, Window
from aiogram_dialog.widgets.input import ManagedTextInput, TextInput
from aiogram_dialog.widgets.kbd import (Back, Button, Calendar, CalendarConfig,
                                        ScrollingGroup, Select, SwitchTo)
from aiogram_dialog.widgets.text import Const, Format

from bot.src.dialogs.functions.functions import (
    delete_category_handler, on_create_category_from_categories)
from bot.src.dialogs.functions.getters import getter_manage_categories
from bot.src.fsm.todoFSM import todoFSM

manage_category_window = Window(
    Const(
        "🗂 Управление категориями. \n\nНажмите на название категории, если хотите её удалить\n\n"
        "Для добавления новой - воспользуйтесь кнопкой ниже"
    ),
    ScrollingGroup(
        Select(
            Format("❌ {item[name]}"),
            items="categories",
            item_id_getter=lambda cat: cat["id"],
            id="category_delete",
            on_click=delete_category_handler,
        ),
        id="manage_scroll",
        width=1,
        height=5,
    ),
    SwitchTo(
        Const("✍️ Добавить категорию"), id="add_new_category", state=todoFSM.add_category
    ),
    SwitchTo(Const("🔙 Назад"), id="back_from_manage_categories", state=todoFSM.start),
    getter=getter_manage_categories,
    state=todoFSM.manage_category,
)
add_category_window = Window(
    Const("Введите название новой категории"),
    TextInput(
        id="new_category_input",
        type_factory=lambda text: text,
        on_success=on_create_category_from_categories,
    ),
    Back(Const("🔙 Назад")),
    state=todoFSM.add_category,
)
