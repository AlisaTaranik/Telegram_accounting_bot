from aiogram.types import Message, CallbackQuery
from aiogram.filters import BaseFilter
from dictionaries import add_dictionary


# this filter is used to catch message with a list of categories to add
class IsCategoriesListFilter(BaseFilter):
    async def __call__(self, message: Message) -> bool:
        text = message.text
        last_word1 = text[-3:]
        last_word2 = text[-8:]
        if last_word1 in add_dictionary.values() or last_word2 in add_dictionary.values():
            return True
        return False


# this filter is used to check if the callback data is from the deleting categories keyboard
class IsDelCategoryCallbackData(BaseFilter):
    async def __call__(self, callback: CallbackQuery) -> bool:
        return callback.data.endswith('_del')


# this filter is used to catch expenses, which are sent as numbers written in different styles
class IsNumberFilter(BaseFilter):
    async def __call__(self, message: Message) -> bool:
        result = False
        m = message.text
        if m.strip('-').isdigit():
            result = True
        elif '.' in m and len(m.split('.')) == 2:
            counter = 0
            for num in m.strip('-').split('.'):
                if num.isdigit():
                    counter += 1
            if counter == 2:
                result = True
        elif ',' in m and len(m.split(',')) == 2:
            counter = 0
            for num in m.strip('-').split(','):
                if num.isdigit():
                    counter += 1
            if counter == 2:
                result = True
        return result


# this filter is used to check if the callback data is from the adding categories keyboard
class IsCategoryCallbackData(BaseFilter):
    async def __call__(self, callback: CallbackQuery) -> bool:
        return callback.data.endswith('_categ')
