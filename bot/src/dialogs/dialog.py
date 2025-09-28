from aiogram_dialog import Dialog

from .windows.archive import (view_archive_task_detail_window,
                              view_archive_window)
from .windows.category import add_category_window, manage_category_window
from .windows.command import commands_window
from .windows.tasks import (add_tasks_window, confirm_task_window,
                            input_description_window, input_time_window,
                            my_tasks_window, pick_category_window,
                            pick_date_window, task_detail_window,
                            task_list_by_category_window,
                            tasks_by_category_window,
                            update_task_description_window)

tasks_dialog = Dialog(
    commands_window,
    my_tasks_window,
    add_tasks_window,
    pick_date_window,
    pick_category_window,
    input_description_window,
    input_time_window,
    confirm_task_window,
    tasks_by_category_window,
    task_list_by_category_window,
    task_detail_window,
    update_task_description_window,
    manage_category_window,
    add_category_window,
    view_archive_window,
    view_archive_task_detail_window,
)
