# there are all words, phrases and messages, which bot uses for communication and which should be translated

# messages and notifications
start_message_text = 'Hello, this is a bot for recording your expenses\nTo know how it works press /help\nDefault language is English. To change language, press /language\n\nПривет, это бот для ведения ваших расходов\nДля получения информации о работе бота нажмите /help\nПо умолчанию язык бота - английский, для изменения языка нажмите /language'
language_message_text = 'Choose the language\nВыберите язык'
language_was_changed = {'RU': 'Язык был изменён на русский',
                        'EN': 'Language was changed to English'}
help_message_text = {'RU': 'Для того, чтобы добавить расход - просто пришлите его в чат. В ответ будет предложено выбрать одну из категорий расходов\nЕсли расход был внесён по ошибке - пришлите его со знаком минус. Например, после внесения расхода "236,98" пришлите в чат "-236,98" для его обнуления (в течение того же месяца и в одну и ту же категорию)\nДобавить или изменить категории расходов можно в разделе categories главного меню. По умолчанию все расходы заносятся в категорию "Другое". Названия категорий сохраняются на том языке, на котором были занесены, за исключением категории "Другое"\nПолучить отчёт о расходах можно в разделе report главного меню. В отчёте будет информация о суммах расходов по годам, месяцам и категориям',
                     'EN': 'To add an expense, just send it in the chat. You will be prompted to choose one of the expense categories in response.\nIf an expense was entered by mistake, send it with a minus sign. For example, after sending "236.98," send "-236.98" in the chat to cancel it (within the same month and in the same category).\nYou can add or change expense categories in the categories section of the main menu. By default, all expenses are recorded in the "Other" category. Category names are saved in the language they were entered, except for the "Other" category.\nTo get an expense report, go to the report section of the main menu. The report will provide information on expense amounts by year, month, and category'}
categories_message_text = {'RU': 'Вы можете просмотреть текущие категории расходов, удалить ненужные или добавить новые',
                           'EN': 'You can check current categories, delete some of them or add new categories'}
deleting_unique_categ_text = {'RU': 'У вас только одна категория расходов, и её нельзя удалить',
                              'EN': "You have only one category and can't delete it"}
deleting_categ_text = {'RU': 'Нажмите на кнопку с категорией, которую хотите удалить',
                       'EN': 'To delete the category press the button with its name'}
ending_categories_text = {'RU': 'Не осталось категорий. Ваши расходы будут по умолчанию вноситься в "Другое"\nЕсли хотите продолжить редактирование - нажмите /categories\nЧтобы зафиксировать расход, пришлите его в чат ',
                          'EN': "You don't have any categories. Your expenses will be recorded as 'Other'\nTo continue editing press /categories\nTo add an expense just send it in the chat"}
finishing_deleting_categ_text = {'RU': 'Удаление категорий завершено',
                                 'EN': 'Deleting was finished'}
adding_categ_text = {'RU': 'Напишите через запятую категории, которые хотите добавить, и в конце слово "добавить"',
                     'EN': 'Please write categories you would like to add separating them by comma and write "add" at the end'}
added_new_categ_text = {'RU': 'Новые категории добавлены',
                        'EN': 'New categories were added'}
to_send_expense_text = {'RU': 'Чтобы зафиксировать расход - пришлите его в чат',
                        'EN': 'To add an expense just send it in the chat'}
to_get_report_text = {'RU': 'Чтобы получить отчёт, нажмите кнопку "Получить отчёт за всё время"',
                      'EN': 'To get the report, press the button "Get full report"'}
dont_have_expenses_text = {'RU': 'В базе данных нет зафиксированных расходов',
                           'EN': 'There are no recorded expenses in the database'}
to_choose_categ_text = {'RU': 'Выберите категорию расходов',
                        'EN': 'Choose the category for this expense'}
expense_was_gotten_text = {'RU': 'Расход внесён в базу данных',
                           'EN': 'Expense was added to database'}
wrong_message_text = {'RU': 'Пожалуйста, присылайте в чат только числа - ваши расходы',
                      'EN': 'Please send only expense amounts in this chat'}

# main menu
help_description = 'help/помощь'
categories_description = 'categories/категории'
report_description = 'report/отчёт'
language_description = 'languages/языки'

# keyboards
check_cat_button_text = {'RU': 'Посмотреть категории', 'EN': 'Check categories'}
delete_cat_button_text = {'RU': 'Удалить категории', 'EN': 'Delete categories'}
add_cat_button_text = {'RU': 'Добавить категории', 'EN': 'Add categories'}
close_editing_cat_button_text = {'RU': 'Закрыть редактирование', 'EN': 'Close editing'}
report_button_text = {'RU': 'Получить отчёт за всё время', 'EN': 'Get full report'}
close_button = {'RU': 'Закрыть', 'EN': 'Close'}

# other dictionaries
add_dictionary = {'RU': 'добавить', 'EN': 'add'}
other = {'RU': 'Другое', 'EN': 'Other'}
your_categories = {'RU': 'Ваши категории', 'EN': 'Your categories'}

report_text = {'RU': '<b>Отчёт за всё время</b>\n<b>Год | Месяц | Категория | Расходы</b>\n',
               'EN': '<b>Full report</b>\n<b>Year | Month | Category | Expenses</b>\n'}

months = {'RU': {1: 'Январь', 2: 'Февраль', 3: 'Март', 4: 'Апрель',
                 5: 'Май', 6: 'Июнь', 7: 'Июль', 8: 'Август',
                 9: 'Сентябрь', 10: 'Октябрь', 11: 'Ноябрь', 12: 'Декабрь'},
          'EN': {1: 'January', 2: 'February', 3: 'March', 4: 'April',
                 5: 'May', 6: 'June', 7: 'July', 8: 'August',
                 9: 'September', 10: 'October', 11: 'Nowember', 12: 'December'}}

