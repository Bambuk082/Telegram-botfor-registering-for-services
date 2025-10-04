from aiogram import F, Router
from aiogram.types import Message, CallbackQuery, ReplyKeyboardRemove


from aiogram.fsm.context import FSMContext

import app.keyboards.keyboards_map as kb

import database.requests as rq
import database.registration as reg

from .hendlers import back


user_rt = Router()

@user_rt.callback_query(F.data == 'user_reg')
async def create_admin(callback: CallbackQuery, state: FSMContext):
    await state.set_state(reg.Reg_user.name)
    menu = kb.menu_to_keyboard['name_reply'](await rq.get_status(callback.from_user.id))
    await rq.change_list_steps(tg_id=callback.from_user.id, parametrs=['name_reply', 'reg.Reg_user.name'], my_list='registration_back', action='append')
    await callback.answer(text='Введіть ваше ім\'я')
    await callback.message.answer(text='Введіть ваше ім\'я', reply_markup= menu)




@user_rt.message(reg.Reg_user.name)
async def create_admin_name(message: Message, state: FSMContext):
    if message.text == 'Назад🔙':
        await state.clear()
        return await back(message, state)
    elif message.text == 'Вставити ім\'я':
        await state.update_data(name=message.from_user.first_name)
    else:
        await state.update_data(name=message.text)
    await state.set_state(reg.Reg_user.phone_number)
    menu = kb.menu_to_keyboard['phone_number_reply']()
    await rq.change_list_steps(tg_id=message.from_user.id, parametrs=['phone_number_reply', 'reg.Reg_user.phone_number'], my_list='registration_back', action='append')
    await message.answer(text='Введіть ваш номер телефону', reply_markup= menu)


@user_rt.message(reg.Reg_user.phone_number)
async def create_admin_phone_number(message: Message, state: FSMContext):
    if message.text == 'Назад🔙':
        return await back(message, state)
    if message.text:
        await state.update_data(phone_number = message.text)
    else:
        await state.update_data(phone_number=message.contact.phone_number)
    await state.set_state(reg.Reg_user.email)
    menu = kb.menu_to_keyboard['email_reply']()
    await rq.change_list_steps(tg_id=message.from_user.id, parametrs=['email_reply', 'reg.Reg_user.email'], my_list='registration_back', action='append')
    await message.answer(text='Введіть вашу електронну пошту', reply_markup= menu)


@user_rt.message(reg.Reg_user.email)
async def create_admin_email(message: Message, state: FSMContext):
    
    if message.text == 'Назад🔙':
        return await back(message, state)
    elif message.text == 'Пропустити':
        await state.update_data(email='не вказано')
    else:
        await state.update_data(email=message.text)
    data = await state.get_data()
    await message.answer(text='Дякуємо за реєстрацію!!!', reply_markup=ReplyKeyboardRemove())
    menu = kb.menu_to_keyboard['registration_user_end']()
    await message.answer(
        text=(
            f'Name: {data["name"]}\n'
            f'Phone number: {data["phone_number"]}\n'
            f'Email: {data["email"]}'
            ),reply_markup= menu
            )
    await rq.change_list_steps(tg_id=message.from_user.id, parametrs=None, my_list='registration_back', action='clear')


@user_rt.callback_query(F.data == 'change_user')
async def change_data(callback: CallbackQuery, state: FSMContext):
    await callback.answer(text='Оберіть, що хочете змінити 👇')
    menu = kb.menu_to_keyboard['change_data_user']()
    await rq.change_list_steps(tg_id=callback.from_user.id, parametrs=['change_data_user'], my_list='callback_back', action='append')
    await callback.message.edit_reply_markup(reply_markup= menu)


@user_rt.callback_query(F.data == 'confirm_user')
async def confirm_registration(callback: CallbackQuery, state: FSMContext):
    tg_id = callback.from_user.id
    await rq.change_list_steps(tg_id=tg_id, parametrs=None, my_list='back', action='clear')
    await rq.change_list_steps(tg_id=tg_id, parametrs=None, my_list='registration_back', action='clear')
    await rq.change_list_steps(tg_id=tg_id, parametrs=None, my_list='callback_back', action='clear')

    data = await state.get_data()
    data_in_db = await rq.get_registration_data(tg_id)
    name = data.get('change_name') if data.get('change_name') is not None else data.get('name')
    phone_number = data.get('change_phone_number') if data.get('change_phone_number') is not None else data.get('phone_number')
    email = data.get('change_email') if data.get('change_email') is not None else data.get('email')
    new_data = {
    'name': name if name is not None else data_in_db.get('name'),
    'phone_number': phone_number if phone_number is not None else data_in_db.get('phone_number'),
    'email': email if email is not None else data_in_db.get('email'), 
    }
    await rq.save_data_to_db(new_data, callback.from_user.id, is_admin=False)
    await callback.answer(text='Реєстрацію підтверджено',)
    await callback.message.delete_reply_markup()
    
    menu = kb.menu_to_keyboard['menu'](await rq.get_status(callback.from_user.id))
    
    await callback.message.answer(
        text='Дані збережено✅', 
        reply_markup=menu)
    await rq.change_list_steps(tg_id=tg_id, parametrs=['menu'], my_list='back', action='append')
    await state.clear()


# Збереження ім'я
@user_rt.callback_query(F.data == 'user_change_name')
async def save_name(callback: CallbackQuery, state: FSMContext):
    await callback.answer(text='Введіть нове ім\'я')
    await callback.message.answer(text='Введіть нове ім\'я', reply_markup=kb.menu_to_keyboard['change_name']())
    await rq.change_list_steps(tg_id=callback.message.from_user.id, parametrs=['registration_user_end'], my_list='change_data', action='append')
    await state.set_state(reg.Reg_user.change_name)

@user_rt.message(reg.Reg_user.change_name)
async def new_name(message: Message, state: FSMContext):
    if message.text == 'Назад🔙':
        await state.clear()
        return await back(message, state)
    if message.text == 'Вставити ім\'я':
        await state.update_data(change_name=message.from_user.first_name)
    else:
        await state.update_data(change_name = message.text)
    data = await state.get_data()
    data_in_db = await rq.get_registration_data(message.from_user.id)
    name = data.get('change_name') if data.get('change_name') is not None else data.get('name')
    phone_number = data.get('change_phone_number') if data.get('change_phone_number') is not None else data.get('phone_number')
    email = data.get('change_email') if data.get('change_email') is not None else data.get('email')
    await message.answer(text='нове ім\'я збережено✅', reply_markup=ReplyKeyboardRemove())
    await message.answer(text=(
            f'Name: {name if name is not None else data_in_db.get('name')}\n'
            f'Phone number: {phone_number if phone_number is not None else data_in_db.get('phone_number')}\n'
            f'Email: {email if email is not None else data_in_db.get('email')}'
            ), reply_markup= kb.menu_to_keyboard['registration_user_end']())
    await rq.change_list_steps(tg_id=message.from_user.id, parametrs=None, my_list='change_data', action='clear')
    

# Зміна номеру телефону
@user_rt.callback_query(F.data == 'user_change_phone_number')
async def save_phone_number(callback: CallbackQuery, state: FSMContext):
    await callback.answer(text='Введіть новий номер телефону')
    await callback.message.answer(text='Введіть новий номер телефону', reply_markup=kb.menu_to_keyboard['change_phone_number']())
    await rq.change_list_steps(tg_id=callback.message.from_user.id, parametrs=['registration_user_end'], my_list='change_data', action='append')
    await state.set_state(reg.Reg_user.change_phone_number)
    print('я тут')

@user_rt.message(reg.Reg_user.change_phone_number)
async def new_phone_number(message: Message, state: FSMContext):
    if message.text == 'Назад🔙':
        await state.clear()
        return await back(message, state)
    if message.text:
        await state.update_data(change_phone_number = message.text)
    else:
        await state.update_data(change_phone_number=message.contact.phone_number)
    
    data = await state.get_data()
    data_in_db = await rq.get_registration_data(message.from_user.id)
    name = data.get('change_name') if data.get('change_name') is not None else data.get('name')
    phone_number = data.get('change_phone_number') if data.get('change_phone_number') is not None else data.get('phone_number')
    email = data.get('change_email') if data.get('change_email') is not None else data.get('email')
    await message.answer(text='новий номер телефону збережено✅', reply_markup=ReplyKeyboardRemove())
    await message.answer(text=(
            f'Name: {name if name is not None else data_in_db.get('name')}\n'
            f'Phone number: {phone_number if phone_number is not None else data_in_db.get('phone_number')}\n'
            f'Email: {email if email is not None else data_in_db.get('email')}'
            ), reply_markup= kb.menu_to_keyboard['registration_user_end']())
    await rq.change_list_steps(tg_id=message.from_user.id, parametrs=None, my_list='change_data', action='clear')


# Зміна електронної пошти
@user_rt.callback_query(F.data == 'user_change_email')
async def save_email(callback: CallbackQuery, state: FSMContext):
    await callback.answer(text='Введіть нову електрону пошту')
    await callback.message.answer(text='Введіть нову електрону пошту', reply_markup=kb.menu_to_keyboard['change_email']())
    await rq.change_list_steps(tg_id=callback.message.from_user.id, parametrs=['registration_user_end'], my_list='change_data', action='append')
    await state.set_state(reg.Reg_user.change_email)

@user_rt.message(reg.Reg_user.change_email)
async def new_email(message: Message, state: FSMContext):
    if message.text == 'Назад🔙':
        return await back(message, state)
    elif message.text == 'Пропустити':
        await state.update_data(email='не вказано')
    else:
        await state.update_data(email=message.text)
    await state.update_data(change_email = message.text)
    data = await state.get_data()
    data_in_db = await rq.get_registration_data(message.from_user.id)
    name = data.get('change_name') if data.get('change_name') is not None else data.get('name')
    phone_number = data.get('change_phone_number') if data.get('change_phone_number') is not None else data.get('phone_number')
    email = data.get('change_email') if data.get('change_email') is not None else data.get('email')
    await message.answer(text='нову пошту збережено✅', reply_markup=ReplyKeyboardRemove())
    await message.answer(text=(
            f'Name: {name if name is not None else data_in_db.get('name')}\n'
            f'Phone number: {phone_number if phone_number is not None else data_in_db.get('phone_number')}\n'
            f'Email: {email if email is not None else data_in_db.get('email')}'
            ), reply_markup= kb.menu_to_keyboard['registration_user_end']())
    await rq.change_list_steps(tg_id=message.from_user.id, parametrs=None, my_list='change_data', action='clear')
    
