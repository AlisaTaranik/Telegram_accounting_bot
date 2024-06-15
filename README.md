
This is a Telegram bot to manage self-accounting.

With the help of this bot, users can save expenses, assign categories to them, change these categories, and receive a report on expenses. Currently, the bot supports two languages: English and Russian.

The bot is written in Python using the aiogram library and built-in libraries. Expense data, categories, and settings are saved in a database implemented with SQLite3. You can find the database schema in this repository.


Near-term development plans for the project:
- add different types of reports (for different periods, comparison with the previous period, with or without categorization);
- add various visualizations for different types of reports;
- set up logging;
- deploy the bot.
  
In the future, I would like to add income tracking, support for different currencies and automatic conversion, add other languages, consider other database options, and optimize working with them
