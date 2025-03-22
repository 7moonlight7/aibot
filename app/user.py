from urllib.parse import uses_relative

from aiogram import Router, F, types
from aiogram.types import Message, CallbackQuery, InputFile
from aiogram.filters import CommandStart, Command
from aiogram.fsm.context import FSMContext
from aiogram.types import BufferedInputFile

import base64
from io import BytesIO

# from app.database.requests import set_user
from app.database.requests import save_image_to_db, get_user_history
# from middlewares import BaseMiddleware


from app.generators import generate
from app.states import Work
import app.keyboards.inline as inl
from app.kardinskiy_photo import generatee, get_model, check_generation
from app.styles import get_styles

user = Router()


@user.message(CommandStart())
async def cmd_start(message: Message):
    # await set_user(message.from_user.id)
    await message.answer('Добро пожаловать в бот!', reply_markup=inl.main)


@user.message(Command('history'))
async def show_history(message: types.Message):
    user_images = await get_user_history(message.from_user.id)

    if user_images:
        for user_image in user_images:
            image_stream = BytesIO(user_image.image)
            input_file = BufferedInputFile(file=image_stream.getvalue(), filename=f'image_{user_image.id}.png')
            caption = f"Изображение от {user_image.created_at}\nПромт: {user_image.promt}"
            await message.answer_photo(input_file, caption=caption)
    else:
        await message.answer("Ваша история пуста.")




@user.callback_query(F.data == 'ai')
async def answer(callback: CallbackQuery, state: FSMContext):
    await callback.message.answer('Введите, что хотите попросить у ИИ.')
    await state.set_state(Work.text)


@user.message(Work.text)
async def ai(message: Message, state: FSMContext):
    res = await generate(message.text)
    await message.answer(res.choices[0].message.content)
    await state.clear()

@user.callback_query(F.data == 'to_main')
async def main(callback: CallbackQuery):
    await callback.message.answer('Добро пожаловать в бот!', reply_markup=inl.main)

@user.callback_query(F.data == 'photo_generate')
async def answer(callback: CallbackQuery, state: FSMContext):
    await callback.message.answer('Какой стиль хотите использовать: ', reply_markup=inl.styles)

@user.callback_query(F.data == 'previous_page')
async def previous_page(callback: CallbackQuery, state: FSMContext):
    await callback.message.answer('Какой стиль хотите использовать: ', reply_markup=inl.styles)

@user.callback_query(F.data == 'default_style')
async def default(callback: CallbackQuery, state: FSMContext):
    all_styles = get_styles()
    for styles in all_styles:
        if styles['name'] == 'DEFAULT':
            await state.update_data(style_name=styles['name'])
            await callback.message.answer_photo(styles['image'], caption='Пример стиля.', reply_markup=inl.ready_or_back)

@user.callback_query(F.data == 'anime_style')
async def anime(callback: CallbackQuery, state: FSMContext):
    all_styles = get_styles()
    for styles in all_styles:
        if styles['name'] == 'ANIME':
            await state.update_data(style_name=styles['name'])
            await callback.message.answer_photo(styles['image'], caption='Пример стиля.', reply_markup=inl.ready_or_back)

@user.callback_query(F.data == 'kardinskiy_style')
async def kandisky(callback: CallbackQuery, state: FSMContext):
    all_styles = get_styles()
    for styles in all_styles:
        if styles['name'] == 'KANDINSKY':
            await state.update_data(style_name=styles['name'])
            await callback.message.answer_photo(styles['image'], caption='Пример стиля.', reply_markup=inl.ready_or_back)

@user.callback_query(F.data == 'detailed_style')
async def kandisky(callback: CallbackQuery, state: FSMContext):
    all_styles = get_styles()
    for styles in all_styles:
        if styles['name'] == 'UHD':
            await state.update_data(style_name=styles['name'])
            await callback.message.answer_photo(styles['image'], caption='Пример стиля.', reply_markup=inl.ready_or_back)

@user.callback_query(F.data == 'start_generate')
async def choice_of_generate(callback: CallbackQuery, state: FSMContext):
    await callback.message.answer("Напишите, что хотите сгенерировать: ")
    await state.set_state(Work.photo)

@user.message(Work.photo)
async def generate_photo(message: Message, state: FSMContext):
        await message.answer("Идет процесс генерации изображения...")
        data = await state.get_data()
        styles_name = str(data.get('style_name'))
        promt = message.text
        model_id = get_model()
        uuid = generatee(promt, model_id, styles_name)
        images = check_generation(uuid)

        if images:
            image_data = base64.b64decode(images[0])
            with open("generated_image.png", "wb") as file:
                file.write(image_data)

            image_stream = BytesIO(image_data)
            image_stream.seek(0)
            input_file = BufferedInputFile(file=image_stream.getvalue(), filename='generated_image.png')
            await save_image_to_db(message.from_user.id, image_data, promt)
            await message.answer_photo(input_file, caption="Вот ваше изображение!", reply_markup=inl.back)
        else:
            await message.answer("Не удалось сгенерировать изображение.")
        await state.clear()

