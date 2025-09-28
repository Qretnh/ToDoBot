from aiogram.fsm.state import State, StatesGroup


class todoFSM(StatesGroup):
    start = State()

    add_category = State()
    manage_category = State()

    my_tasks = State()
    add_task = State()
    task_list_by_category = State()
    tasks_by_category = State()
    pick_date = State()
    pick_category = State()
    input_description = State()
    input_time = State()
    update_task_description = State()
    confirm_task = State()

    view_archive = State()
    task_detail = State()
    view_archive_task_detail = State()
