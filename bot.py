import os
from aiogram import Bot, Dispatcher, types
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram import F
from aiogram.types import WebAppInfo
from aiogram import Router
from aiogram import executor

TOKEN = os.getenv("BOT_TOKEN")
WEBAPP_URL = os.getenv("WEBAPP_URL")

bot = Bot(token=TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.HTML))
dp = Dispatcher()

router = Router()
dp.include_router(router)

@router.message(F.text == "/start")
async def start(msg: types.Message):
    kb = InlineKeyboardBuilder()
    kb.button(text="Открыть WebApp", web_app=WebAppInfo(url=f"{WEBAPP_URL}/index.html"))
    await msg.answer("Открываю WebApp", reply_markup=kb.as_markup())

if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
