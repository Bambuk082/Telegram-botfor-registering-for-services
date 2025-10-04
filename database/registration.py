from aiogram.fsm.state import State, StatesGroup

class Reg_user(StatesGroup):
    name = State()
    phone_number = State()
    email = State()

    change_name = State()
    change_phone_number = State()
    change_email = State()

class Reg_admin(StatesGroup):
    name = State()
    phone_number = State()
    email = State()
    
    change_name = State()
    change_phone_number = State()
    change_email = State()

class Change_contact(StatesGroup):
    change_name = State()
    change_phone_number = State()
    change_email = State()
