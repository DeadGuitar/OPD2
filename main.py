import asyncio
import logging
from drugparse import parse
import sys
from os import getenv

from aiogram import Bot, Dispatcher, html, F
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram.filters import CommandStart
from aiogram.filters import Command
from aiogram.types import Message, InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram.utils.keyboard import ReplyKeyboardBuilder
from aiogram.types import CallbackQuery


TOKEN = "6901890428:AAG6B3QksLX9pv921mZzXmmM1UjIz0hFILM"

dp = Dispatcher()

@dp.message(CommandStart())
async def command_start_handler(message: Message) -> None:

    await message.answer(f"Здравствуйте, {html.bold(message.from_user.full_name)}!\nЭтот бот поможет вам найти препараты в аптеках Омска.\nДля поиска просто введите название лекарства.")


@dp.message(Command("help"))
async def command_help_handler(message: Message) -> None:
    await message.answer(f"Чтобы найти препарат, просто введите его название")


@dp.message()
async def searcher(message: Message) -> None:
    f = open('SearcersSearches.txt', 'a')
    f.write(f"@{message.chat.username}({message.from_user.url}) искал {message.text}\n")
    print(f"@{message.chat.username} искал {message.text}")
    f.close
    if len(message.text)<3: await message.answer(f"Введите не менее трёх символов для поиска")
    else:
        dumm = await message.answer(f"Поиск...")
        item = parse(message.text)
        await dumm.delete()
        i = 0

        if item != 0:
            builder = InlineKeyboardBuilder()
            # builder.add(InlineKeyboardButton(text="<<", callback_data="back"), InlineKeyboardButton(text=">>", callback_data="forward"))
            builder.add(InlineKeyboardButton(text="Больше информации", url=f"{item[2][i]}"))
            showcase = await message.reply_photo(item[3][i],f'{item[0][i]}\nЦена: от {item[1][i]}₽\nсмартфон vivo', parse_mode=ParseMode.HTML, reply_markup=builder.as_markup())
        else:
            showcase = await message.reply_photo("https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcQ-q2ATqFNFdX8CMLis6rc49Pt9HFW3SFhZJyXAjYshYw&s", f'Увы, по вашему запросу ничего не найдено...\nсмартфон vivo',)
#@dp.callback_query()
#async def NextOrPrevious(callback: CallbackQuery):
#    action = callback.data
#    print(action)
#    if action == "forward":
#        i+=1
#        await showcase.edit_text(f'{item[0][i]}\nЦена: от {item[1][i]}₽\nЭта карочи уже почти не заглушка', parse_mode=ParseMode.HTML, reply_markup=builder.as_markup())

async def main() -> None:
    # Initialize Bot instance with default bot properties which will be passed to all API calls
    bot = Bot(token=TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.HTML))
    # And the run events dispatching
    await dp.start_polling(bot)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    asyncio.run(main())
    