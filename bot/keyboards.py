from aiogram import Bot
from aiogram.types import BotCommand
from aiogram.types import InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder
from dictionaries import *


# main menu
async def set_main_menu(bot: Bot):
    main_menu_commands = [BotCommand(command=command,
                                     description=description)
                        for command, description in
                          {'help': help_description,
                           'language': language_description,
                           'categories': categories_description,
                           'report': report_description}.items()]
    await bot.set_my_commands(main_menu_commands)


# inline keyboard for language settings
def language_settings_kb():
    ru_button = InlineKeyboardButton(text='Русский',
                                     callback_data='RU')
    en_button = InlineKeyboardButton(text='English',
                                     callback_data='EN')
    kb_builder = InlineKeyboardBuilder()
    kb_builder.row(ru_button, en_button)
    return kb_builder.as_markup()


# inline keyboard for checking and editing categories
def categories_settings_kb(lang):
    kb_builder = InlineKeyboardBuilder()
    kb_builder.row(InlineKeyboardButton(text=check_cat_button_text[lang],
                                        callback_data='check_categories'))
    kb_builder.row(InlineKeyboardButton(text=delete_cat_button_text[lang],
                                        callback_data='delete_categories'))
    kb_builder.row(InlineKeyboardButton(text=add_cat_button_text[lang],
                                        callback_data='add_categories'))
    kb_builder.row(InlineKeyboardButton(text=close_editing_cat_button_text[lang],
                                        callback_data='close_editing_categories'))
    return kb_builder.as_markup()


# inline keyboard for deleting categories
def delete_categories_kb(categories_list, lang):
    kb_builder = InlineKeyboardBuilder()
    for category in sorted(categories_list):
        kb_builder.row(InlineKeyboardButton(text=f'❌ - {category}',
                                            callback_data=f'{category}_del'))
    kb_builder.row(InlineKeyboardButton(text=close_button[lang],
                                        callback_data='cancel_deleting_categories'))
    return kb_builder.as_markup()


# inline keyboard for choosing category while adding expense to the database
def add_category_to_expense_kb(categories_list):
    kb_builder = InlineKeyboardBuilder()
    for category in sorted(categories_list):
        kb_builder.row(InlineKeyboardButton(text=f'{category}',
                                            callback_data=f'{category}_categ'))
    return kb_builder.as_markup()


# inline keyboard to confirm getting report
def get_report_kb(lang):
    kb_builder = InlineKeyboardBuilder()
    kb_builder.row(InlineKeyboardButton(text=report_button_text[lang],
                                        callback_data='get_full_report'))
    return kb_builder.as_markup()
