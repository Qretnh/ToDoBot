import logging

from aiogram import Dispatcher
from aiogram_dialog import DialogManager
from environs import Env

from bot.src.services.api.categories import get_categories
from bot.src.services.api.tasks import get_tasks

env = Env()
env.read_env()

BASE_URL = env("API_BASE_URL")

DEFAULT_TIME = "18:00"


async def getter_categories(dialog_manager: DialogManager, **kwargs):
    categories = await get_categories(dialog_manager.start_data["user_id"])
    dialog_manager.dialog_data["categories"] = categories
    return {"categories": categories}


async def getter_task(dialog_manager: DialogManager, **kwargs):
    return {
        "task": dialog_manager.dialog_data["task"],
        "created_at": dialog_manager.dialog_data["task"]["created_at"][:10],
        "due_date": dialog_manager.dialog_data["task"]["due_date"][:10],
    }


async def getter_tasks_data(dialog_manager: DialogManager, **kwargs):
    user_id = dialog_manager.start_data["user_id"]
    tasks = await get_tasks(user_id)
    actual_tasks = [task for task in tasks if task["is_completed"] == False]
    logging.getLogger(__name__).debug(f"Tasks fetched: {tasks}")
    formatted = "\n".join(
        [
            f"📌 {task['title']}\n"
            f"<i>(Создано {task['created_at'][:10]})</i>\n"
            f"Категория: <b>{task['category']['name']}</b>\n"
            f"Описание: <b>{task['description']}</b>\n"
            f"Дата исполнения: <b>{task['due_date'][:10]} {task['due_time'][:5]}</b>\n"
            for task in actual_tasks
        ]
    )
    return {"tasks_text": formatted or "Нет задач 💤"}


async def getter_confirm_task(
    dialog_manager: DialogManager, dispatcher: Dispatcher, **kwargs
):
    return {
        "title": dialog_manager.dialog_data.get("title"),
        "due_date": dialog_manager.dialog_data.get("due_date"),
        "description": dialog_manager.dialog_data.get("description"),
        "due_time": dialog_manager.dialog_data.get("due_time")[:5],
    }


async def getter_tasks_by_category(dialog_manager: DialogManager, **kwargs):
    user_id = dialog_manager.start_data["user_id"]
    tasks = await get_tasks(user_id)

    categories = {}
    for task in tasks:
        cat = task["category"]["name"] if task["category"] else "Без категории"
        if cat not in categories:
            categories[cat] = []
        categories[cat].append(task)

    return {"grouped_tasks": categories}


async def getter_selected_category_tasks(dialog_manager: DialogManager, **kwargs):
    user_id = dialog_manager.start_data["user_id"]
    tasks = await get_tasks(user_id)
    tasks = [task for task in tasks if task["is_completed"] == False]
    selected_category = dialog_manager.dialog_data["selected_category"]
    filtered = [
        task
        for task in tasks
        if (task["category"] and task["category"]["name"] == selected_category)
        or (not task["category"] and selected_category == "Без категории")
    ]

    dialog_manager.dialog_data["TODO"] = {selected_category: filtered}

    return {"TODO": filtered, "category": selected_category}


async def getter_manage_categories(dialog_manager: DialogManager, **kwargs):
    user_id = dialog_manager.start_data["user_id"]
    categories = await get_categories(user_id)
    return {"categories": categories}


async def getter_archive(dialog_manager: DialogManager, **kwargs):
    user_id = dialog_manager.start_data["user_id"]
    tasks = await get_tasks(user_id)

    tasks = [task for task in tasks if task["is_completed"]]
    dialog_manager.dialog_data["archive_tasks"] = tasks

    return {"tasks": tasks}
