import asyncio
from io import BytesIO
from PIL import Image, ImageFilter
import pytesseract
from aiogram import Bot, Dispatcher, executor, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup

pytesseract.pytesseract.tesseract_cmd = '<full_path_to_your_tesseract_executable>'
API_TOKEN = ''
tags = ["@elonmusk", "Elon", "Musk", "ETH", "BTC"]
wait = 30

bot = Bot(token=API_TOKEN)
storage = MemoryStorage()
dp = Dispatcher(bot, storage=storage)


class States(StatesGroup):
    new_member = State()


@dp.message_handler(content_types="photo", state=States.new_member)
async def photo_with_musk(message: types.Message, state: FSMContext):
    check = await is_musk(message)
    if check:
        await message.delete()


@dp.message_handler(content_types='new_chat_members')
async def new_chat_members(message: types.Message, state: FSMContext):
    asyncio.get_event_loop().call_later(wait, asyncio.create_task, state.finish())
    await States.new_member.set()


async def is_musk(message: types.Message):
    file = BytesIO()
    await message.photo[-1].download(destination=file)
    img = Image.open(file)
    img = img.filter(ImageFilter.SMOOTH_MORE)
    text = pytesseract.image_to_string(img, lang="eng")
    return all(j in text for j in tags)


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
