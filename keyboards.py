from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup


# ===== Main Menu buttons =====
current_course_btn = InlineKeyboardButton('Узнать текущий курс', callback_data='course_btn')
info_btn = InlineKeyboardButton('Информация', callback_data='info_btn')
menu_keyboard = InlineKeyboardMarkup(row_width=1).add(current_course_btn, info_btn)


# ===== Back button =====
back_btn = InlineKeyboardButton('Назад', callback_data='back_btn')
back_keyboard = InlineKeyboardMarkup().add(back_btn)
