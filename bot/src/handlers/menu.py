import aiogram_dialog
from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message
from aiogram_dialog import DialogManager
from src.services.api.users import register_user

from bot.src.fsm.todoFSM import todoFSM

router = Router()


@router.message(Command(commands=["start"]))
async def menu(message: Message, dialog_manager: DialogManager):
    await register_user(str(message.from_user.id), message.from_user.username)
    await dialog_manager.start(todoFSM.start, data={"user_id": message.from_user.id})
