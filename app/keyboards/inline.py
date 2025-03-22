from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

main = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text='ИИ',callback_data='ai'), InlineKeyboardButton(text='Генерация фото', callback_data='photo_generate')]
])

styles = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text='DEFAULT', callback_data='default_style'),
     InlineKeyboardButton(text='KANDINSKY', callback_data='kardinskiy_style')],
    [InlineKeyboardButton(text='DETAILED', callback_data='detailed_style'),
     InlineKeyboardButton(text='ANIME', callback_data='anime_style')],
    [InlineKeyboardButton(text='НАЗАД', callback_data='to_main')]
])

ready_or_back = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text='СТАРТ', callback_data='start_generate'), InlineKeyboardButton(text='НАЗАД', callback_data='previous_page')]
])

back = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text='НАЗАД', callback_data='to_main')]
])