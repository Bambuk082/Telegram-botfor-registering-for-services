from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.keyboard import ReplyKeyboardBuilder, InlineKeyboardBuilder
from aiogram.types.web_app_info import WebAppInfo
from database.models import User

 



def start_kb():
    kb = InlineKeyboardBuilder()
    kb.add(InlineKeyboardButton(text='Реєстрація', callback_data='user_reg'))
    return kb.adjust(1).as_markup()


def change_data():
    kb = InlineKeyboardBuilder()
    kb.button(text='Змінити⚙', callback_data='change_data')
    return kb.adjust(1).as_markup()

def menu(status: str):
    kb = ReplyKeyboardBuilder()
    if not status == 'admin':
        kb.add(KeyboardButton(text='Записатись', web_app=WebAppInfo(url='https://bambuk082.github.io/site-for-tg-bot/')))
    
    kb.button(text='Мій профіль')
    kb.button(text='Контакти')

    if status == 'admin':
        kb.add(KeyboardButton(text='Для адміністратора'))
        
    kb.adjust(*( (2, 1) if status == 'admin' else (1, 2) ))

    return kb.as_markup(resize_keyboard=True)



def admin_menu(admin_is_created):
    kb = ReplyKeyboardBuilder()
    if admin_is_created:
        kb.button(text='Перезаписати адміністратора')
    
    if not admin_is_created:
        kb.add(KeyboardButton(text='Створити адміністратора'))
    kb.button(text='Назад🔙')

    return kb.adjust(2).as_markup(resize_keyboard=True)
        

def change_data_admin():
    kb = InlineKeyboardBuilder()
    kb.button(text='Змінити ім\'я', callback_data='change_name_admin')
    kb.button(text='Змінити номер телефону', callback_data='change_phone_number_admin')
    kb.button(text='Змінити електронну пошту', callback_data='change_email_admin')
    kb.button(text='Назад', callback_data='back')
    
    return kb.adjust(1).as_markup()

def change_data_user():
    kb = InlineKeyboardBuilder()
    kb.button(text='Змінити ім\'я', callback_data='user_change_name')
    kb.button(text='Змінити номер телефону', callback_data='user_change_phone_number')
    kb.button(text='Змінити електронну пошту', callback_data='user_change_email')
    kb.button(text='Назад', callback_data='back')
    
    return kb.adjust(1).as_markup()


def registration_admin_end():
    kb = InlineKeyboardBuilder()
    kb.button(text='Змінити✏', callback_data='change_admin')
    kb.button(text='Підтвердити!✅', callback_data='confirm_admin')
    
    return kb.adjust(2).as_markup()

def registration_user_end():
    kb = InlineKeyboardBuilder()
    kb.button(text='Змінити✏', callback_data='change_user')
    kb.button(text='Підтвердити!✅', callback_data='confirm_user')
    
    return kb.adjust(2).as_markup()

def registration_contact_end():
    kb = InlineKeyboardBuilder()
    kb.button(text='Змінити✏', callback_data='change_contact')
    kb.button(text='Підтвердити!✅', callback_data='confirm_contact')
    
    return kb.adjust(2).as_markup()

# Реєстрація для адміністратора
class Reg_menu():
    def __init__(self):
        pass
    # Клавіатура для збереження даних реєстрації # 
    def name_reply(self, status):
        kb = ReplyKeyboardBuilder()
        kb.button(text='Вставити ім\'я')
        if status == 'admin':
            kb.button(text='Назад🔙')
        return kb.adjust(2).as_markup(resize_keyboard=True)

    def phone_number_reply(self):
        kb = ReplyKeyboardBuilder()
        kb.button(text='Вставити номер телефону', request_contact=True)
        kb.button(text='Назад🔙')
        return kb.adjust(2).as_markup(resize_keyboard=True)

    def email_reply(self):
        kb = ReplyKeyboardBuilder()
        kb.button(text='Пропустити')
        kb.button(text='Назад🔙')
        return kb.adjust(2).as_markup(resize_keyboard=True)
    
    # Клавіатура для зміни даних реєстрації #
    def change_name_reply(self):
        kb = ReplyKeyboardBuilder()
        kb.button(text='Вставити ім\'я')
        return kb.adjust().as_markup(resize_keyboard=True)

    def change_phone_number_reply(self):
        kb = ReplyKeyboardBuilder()
        kb.button(text='Вставити номер телефону', request_contact=True)
        return kb.adjust().as_markup(resize_keyboard=True)

    def change_email_reply(self):
        kb = ReplyKeyboardBuilder()
        kb.button(text='Пропустити')
        return kb.adjust().as_markup(resize_keyboard=True)


def get_record_date():
    kb = InlineKeyboardBuilder()
    kb.button(text='Отримати', callback_data='get')
    kb.button(text='Назад🔙', callback_data='back')
    
    return kb.adjust(2).as_markup()