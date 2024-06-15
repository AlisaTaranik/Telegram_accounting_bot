import sqlite3 as sq

from aiogram import F, Router
from aiogram.filters import Command

from keyboards import *
from filters import *
from dictionaries import *

router = Router()


# handler for the start command
# it shows a welcome message for user and add them to the database
@router.message(Command(commands='start'))
async def start_command(message: Message):
    await message.answer(text=start_message_text)
    with sq.connect('expense_database.db') as con:
        cur = con.cursor()
        cur.execute("SELECT tg_user_id FROM users")
        tg_id_info = cur.fetchall()
        tg_id_list = list(map(lambda x: x[0], tg_id_info))
        current_id = message.from_user.id
        if current_id not in tg_id_list:
            cur.execute("INSERT INTO users (tg_user_id, user_language) VALUES ('%s', 'EN')" % message.from_user.id)
            cur.execute("SELECT user_id FROM users WHERE tg_user_id = '%s'" % message.from_user.id)
            us_id = cur.fetchall()[0][0]
            cur.execute("INSERT INTO categories (category_name, user_id, category_status) VALUES ('Other', '%s', 1)" % (us_id))
        con.commit()
        cur.close()


# handler for the help command
# it shows a message with info about the bot and how it works
@router.message(Command(commands='help'))
async def help_command(message: Message):
    with sq.connect('expense_database.db') as con:
        cur = con.cursor()
        cur.execute("SELECT user_language FROM users WHERE tg_user_id = '%s'" % message.from_user.id)
        lang = cur.fetchall()[0][0]
        cur.close()
    await message.answer(text=help_message_text[lang])


# handler for the language command
# it asks to choose language and shows an inline keyboard with languages
@router.message(Command(commands='language'))
async def language_command(message: Message):
    await message.answer(text=language_message_text,
                         reply_markup=language_settings_kb())


# this handler catches callback when English language was chosen
@router.callback_query(F.data == 'EN')
async def set_english(callback: CallbackQuery):
    lang = callback.data
    with sq.connect('expense_database.db') as con:
        cur = con.cursor()
        cur.execute("SELECT user_id FROM users WHERE tg_user_id = '%s'" % callback.from_user.id)
        us_id = cur.fetchall()[0][0]
        cur.execute("UPDATE users SET user_language = '%s' WHERE user_id = '%s'" % (lang, us_id))
        cur.execute("UPDATE categories SET category_name = '%s' "
                    "WHERE category_name = '%s' AND user_id = '%s'" % (other['EN'], other['RU'], us_id))
        con.commit()
        cur.close()
    await callback.message.edit_text(text=language_was_changed[lang])


# this handler catches callback when Russian language was chosen
@router.callback_query(F.data == 'RU')
async def set_russian(callback: CallbackQuery):
    lang = callback.data
    with sq.connect('expense_database.db') as con:
        cur = con.cursor()
        cur.execute("SELECT user_id FROM users WHERE tg_user_id = '%s'" % callback.from_user.id)
        us_id = cur.fetchall()[0][0]
        cur.execute("UPDATE users SET user_language = '%s' WHERE user_id = '%s'" % (lang, us_id))
        cur.execute("UPDATE categories SET category_name = '%s' "
                    "WHERE category_name = '%s' AND user_id = '%s'" % (other['RU'], other['EN'], us_id))
        con.commit()
        cur.close()
    await callback.message.edit_text(text=language_was_changed[lang])


# handler for the categories command
# it shows a message with actions which user can do with categories of expenses and offer them a keyboard for that
@router.message(Command(commands='categories'))
async def categories_command(message: Message):
    with sq.connect('expense_database.db') as con:
        cur = con.cursor()
        cur.execute("SELECT user_language FROM users WHERE tg_user_id = '%s'" % message.from_user.id)
        lang = cur.fetchall()[0][0]
        cur.close()
    await message.answer(text=categories_message_text[lang],
                         reply_markup=categories_settings_kb(lang))


# this handler catches callback when user has chosen to check list of categories
# it still shows categories settings keyboard, but changes message above to the list of current user's categories
@router.callback_query(F.data == 'check_categories')
async def check_categories(callback: CallbackQuery):
    with sq.connect('expense_database.db') as con:
        cur = con.cursor()
        cur.execute("SELECT user_id FROM users WHERE tg_user_id = '%s'" % callback.from_user.id)
        us_id = cur.fetchall()[0][0]
        cur.execute("SELECT user_language FROM users WHERE tg_user_id = '%s'" % callback.from_user.id)
        lang = cur.fetchall()[0][0]
        cur.execute("SELECT category_name FROM categories "
                    "WHERE user_id = '%s' AND category_status = 1 ORDER BY category_name" % us_id)
        categories_list = cur.fetchall()
        categories_info = f'<b>{your_categories[lang]}:</b>\n'
        for c in categories_list:
            categ = str(c[0] + '\n')
            categories_info += str(categ)
        cur.close()
    await callback.message.edit_text(text=categories_info,
                                     reply_markup=categories_settings_kb(lang))


# this handler catches callback when user has chosen to add new categories
# it removes keyboard and asks user to send new categories as a message in the chat
@router.callback_query(F.data == 'add_categories')
async def start_adding_categories(callback: CallbackQuery):
    with sq.connect('expense_database.db') as con:
        cur = con.cursor()
        cur.execute("SELECT user_language FROM users WHERE tg_user_id = '%s'" % callback.from_user.id)
        lang = cur.fetchall()[0][0]
        cur.close()
    await callback.message.edit_text(text=adding_categ_text[lang])


# this handler processes info from user's message with new categories
# if these categories were previously into the database for this user, their status changes to active
# if they are absolutely new, handler adds them to the database
@router.message(IsCategoriesListFilter())
async def process_adding_categories(message: Message):
    with sq.connect('expense_database.db') as con:
        cur = con.cursor()
        cur.execute("SELECT user_id FROM users WHERE tg_user_id = '%s'" % message.from_user.id)
        us_id = cur.fetchall()[0][0]
        cur.execute("SELECT user_language FROM users WHERE tg_user_id = '%s'" % message.from_user.id)
        lang = cur.fetchall()[0][0]
        if lang == 'RU':
            s = message.text.lower()[:-9]
        elif lang == 'EN':
            s = message.text.lower()[:-4]
        adding_categories = set([category.strip(' ').capitalize() for category in s.split(',')]) - {'', ' ', '  '}
        cur.execute("SELECT category_name FROM categories WHERE user_id = '%s' AND category_status = 0" % us_id)
        inact_cat_info = cur.fetchall()
        inactive_categories = set(list(map(lambda x: x[0], inact_cat_info)))
        adding_and_inactive_categories = adding_categories & inactive_categories
        for category in adding_and_inactive_categories:
            cur.execute("UPDATE categories SET category_status = 1 "
                        "WHERE user_id = '%s' AND category_name = '%s'" % (us_id, category))
        cur.execute("SELECT category_name FROM categories "
                    "WHERE user_id = '%s' AND category_status = 1 ORDER BY category_name" % us_id)
        act_cat_info = cur.fetchall()
        active_categories = set(list(map(lambda x: x[0], act_cat_info)))
        new_adding_categories = adding_categories - active_categories
        for category in new_adding_categories:
            cur.execute("INSERT INTO categories (category_name, user_id, category_status) "
                        "VALUES ('%s', '%s', 1)" % (category, us_id))
        con.commit()
        cur.close()
    await message.answer(text=added_new_categ_text[lang],
                         reply_markup=categories_settings_kb(lang))


# this handler catches callback when user has chosen to delete categories
# it shows new inline keyboard for deleting categories and asks user to tap on categories which they want to delete
@router.callback_query(F.data == 'delete_categories')
async def start_deleting_categories(callback: CallbackQuery):
    with sq.connect('expense_database.db') as con:
        cur = con.cursor()
        cur.execute("SELECT user_id FROM users WHERE tg_user_id = '%s'" % callback.from_user.id)
        us_id = cur.fetchall()[0][0]
        cur.execute("SELECT user_language FROM users WHERE tg_user_id = '%s'" % callback.from_user.id)
        lang = cur.fetchall()[0][0]
        cur.execute("SELECT category_name FROM categories "
                    "WHERE user_id = '%s' AND category_status = 1 ORDER BY category_name" % us_id)
        categories_info = cur.fetchall()
        categories_list = list(map(lambda x: x[0], categories_info))
        cur.close()
    await callback.message.edit_text(text=deleting_categ_text[lang],
                                     reply_markup=delete_categories_kb(categories_list, lang))


# this handler catches callback when user chose a category to delete in the deleting keyboard
# it removes button from deleting keyboard and change activity status of category in the database to False (0)
# if all categories were deleted, "Other" category's status is changed to active and user gets message about it
@router.callback_query(IsDelCategoryCallbackData())
async def delete_category(callback: CallbackQuery):
    deleting_category = callback.data[:-4]
    with sq.connect('expense_database.db') as con:
        cur = con.cursor()
        cur.execute("SELECT user_id FROM users WHERE tg_user_id = '%s'" % callback.from_user.id)
        us_id = cur.fetchall()[0][0]
        cur.execute("SELECT user_language FROM users WHERE tg_user_id = '%s'" % callback.from_user.id)
        lang = cur.fetchall()[0][0]
        cur.execute("UPDATE categories SET category_status = 0 "
                    "WHERE user_id = '%s' AND category_name = '%s'" % (us_id, deleting_category))
        cur.execute("SELECT category_name FROM categories "
                    "WHERE user_id = '%s' AND category_status = 1 ORDER BY category_name" % us_id)
        categories_info = cur.fetchall()
        categories_list = list(map(lambda x: x[0], categories_info))
        if len(categories_list) == 0:
            cur.execute("UPDATE categories SET category_status = 1 "
                        "WHERE category_name = '%s' AND user_id = '%s'" % (other[lang], us_id))
            con.commit()
            cur.close()
            await callback.message.edit_text(text=ending_categories_text[lang])
        else:
            con.commit()
            cur.close()
            await callback.message.edit_text(text=deleting_categ_text[lang],
                                             reply_markup=delete_categories_kb(categories_list, lang))


# this handler catches callback when user canceled deleting keyboard
# it shows message that deleting was finished and shows categories settings inline keyboard again
@router.callback_query(F.data == 'cancel_deleting_categories')
async def cancel_deleting_category(callback: CallbackQuery):
    with sq.connect('expense_database.db') as con:
        cur = con.cursor()
        cur.execute("SELECT user_language FROM users WHERE tg_user_id = '%s'" % callback.from_user.id)
        lang = cur.fetchall()[0][0]
        cur.close()
    await callback.message.edit_text(text=finishing_deleting_categ_text[lang],
                                     reply_markup=categories_settings_kb(lang))


# this handler catches callback when user has chosen to close editing categories
# it removes categories settings keyboard and offer user to send an expense in the chat
@router.callback_query(F.data == 'close_editing_categories')
async def close_editing_categories(callback: CallbackQuery):
    with sq.connect('expense_database.db') as con:
        cur = con.cursor()
        cur.execute("SELECT user_language FROM users WHERE tg_user_id = '%s'" % callback.from_user.id)
        lang = cur.fetchall()[0][0]
        cur.close()
    await callback.message.edit_text(text=to_send_expense_text[lang])


# this handler processes message with an expense
# it adds the expense to the database with current month/year and shows keyboard for choosing category
@router.message(IsNumberFilter())
async def get_expense(message: Message):
    month_num = int(str(message.date).split('-')[1])
    current_year = int(str(message.date).split('-')[0])
    expense = float(message.text)
    with sq.connect('expense_database.db') as con:
        cur = con.cursor()
        cur.execute("SELECT user_id FROM users WHERE tg_user_id = '%s'" % message.from_user.id)
        us_id = cur.fetchall()[0][0]
        cur.execute("SELECT user_language FROM users WHERE tg_user_id = '%s'" % message.from_user.id)
        lang = cur.fetchall()[0][0]
        current_month = months[lang][month_num]
        cur.execute("SELECT category_name FROM categories "
                    "WHERE user_id = '%s' AND category_status = 1 ORDER BY category_name" % us_id)
        categories_info = cur.fetchall()
        categories_list = list(map(lambda x: x[0], categories_info))
        cur.execute("INSERT INTO expenses (expense, expense_year, expense_month, expense_name_month, user_id, category_id) "
                    "VALUES ('%s','%s','%s', '%s', '%s', 0)" % (expense, current_year, month_num, current_month, us_id))
        con.commit()
        cur.close()
    await message.answer(text=to_choose_categ_text[lang],
                         reply_markup=add_category_to_expense_kb(categories_list=categories_list))


# this handler catches callback when user chose category for the expense
# it adds chosen category to the database, remove the keyboard and shows a message that expense was added
@router.callback_query(IsCategoryCallbackData())
async def add_category_to_expense(callback: CallbackQuery):
    category = str(callback.data[:-6])
    with sq.connect('expense_database.db') as con:
        cur = con.cursor()
        cur.execute("SELECT user_id FROM users WHERE tg_user_id = '%s'" % callback.from_user.id)
        us_id = cur.fetchall()[0][0]
        cur.execute("SELECT user_language FROM users WHERE tg_user_id = '%s'" % callback.from_user.id)
        lang = cur.fetchall()[0][0]
        cur.execute("UPDATE expenses "
                    "SET category_id = (SELECT category_id FROM categories WHERE category_name = '%s')"
                    "WHERE expense_id = (SELECT expense_id FROM expenses ORDER BY expense_id DESC LIMIT 1) "
                    "AND user_id = '%s'" % (category, us_id))
        con.commit()
        cur.close()
    await callback.message.edit_text(expense_was_gotten_text[lang])


# handler for the report command
# it shows a keyboard for reports and offer to get a full report
@router.message(Command(commands='report'))
async def report_command(message: Message):
    with sq.connect('expense_database.db') as con:
        cur = con.cursor()
        cur.execute("SELECT user_language FROM users WHERE tg_user_id = '%s'" % message.from_user.id)
        lang = cur.fetchall()[0][0]
        cur.close()
    await message.answer(text=to_get_report_text[lang],
                         reply_markup=get_report_kb(lang))


# this handler catches callback when user press the button "get full report"
# it removes keyboard and change the message to the text with all expenses of the user
# expenses are taken from the database and shown categorized by years, months and categories
@router.callback_query(F.data == 'get_full_report')
async def get_full_report(callback: CallbackQuery):
    with sq.connect('expense_database.db') as con:
        cur = con.cursor()
        cur.execute("SELECT user_id FROM users WHERE tg_user_id = '%s'" % callback.from_user.id)
        us_id = cur.fetchall()[0][0]
        cur.execute("SELECT user_language FROM users WHERE tg_user_id = '%s'" % callback.from_user.id)
        lang = cur.fetchall()[0][0]
        cur.execute("SELECT expense_year, expense_name_month, category_name, SUM(expense) AS total_expenses "
                    "FROM expenses JOIN categories USING(category_id) "
                    "WHERE expenses.user_id = '%s' "
                    "GROUP BY expense_year, expense_name_month, category_name "
                    "ORDER BY expense_year, expense_month, category_name" % us_id)
        report_info = cur.fetchall()
        cur.close()
    report = report_text[lang]
    if len(report_info) != 0:
        for line in report_info:
            new_line = ' | '.join([str(i) for i in line]) + '\n'
            report += new_line
        await callback.message.edit_text(text=report)
    else:
        await callback.message.edit_text(text=dont_have_expenses_text[lang])


# this handler processes all other messages
@router.message()
async def other_updates(message: Message):
    with sq.connect('expense_database.db') as con:
        cur = con.cursor()
        cur.execute("SELECT user_language FROM users WHERE tg_user_id = '%s'" % message.from_user.id)
        lang = cur.fetchall()[0][0]
        cur.close()
    await message.answer(text=wrong_message_text[lang])
