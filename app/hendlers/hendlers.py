from aiogram import F, Router
from aiogram.types import Message, CallbackQuery, ReplyKeyboardRemove
from aiogram.filters import Command, CommandStart
import json
import aiosmtplib, asyncio
from email.message import EmailMessage

from aiogram.fsm.context import FSMContext

import app.keyboards.keyboards_map as kb
import database.registration as reg
import database.requests as rq
  


rt = Router()



async def back(message, state: FSMContext):
    
    text = ''
    value: object = None
    tg_id = message.from_user.id
    status = await rq.get_status(tg_id)
    admin_exists = await rq.admin_is_created()
    fsm = None
    
    
    if await rq.change_list_steps(tg_id=tg_id, parametrs=None, my_list='registration_back', action=None, is_exists=True):
        await rq.change_list_steps(tg_id=tg_id, parametrs=None, my_list='registration_back', action='pop')
        if await rq.change_list_steps(tg_id=tg_id, parametrs=None, my_list='registration_back', action=None, is_exists=True):
    
            e = await rq.change_list_steps(tg_id=tg_id, parametrs=None, my_list='registration_back', action=None, is_exists=True, arr_index=-1)
            k = e[0] if e else []
            st = e[-1] if e else []
            
            match st:
                case 'reg.Reg_admin.name': fsm = reg.Reg_admin.name
                case 'reg.Reg_admin.phone_number': fsm = reg.Reg_admin.phone_number
                case 'reg.Reg_admin.email': fsm = reg.Reg_admin.email
                case 'reg.Reg_user.name': fsm = reg.Reg_user.name
                case 'reg.Reg_user.phone_number': fsm = reg.Reg_user.phone_number
                case 'reg.Reg_user.email': fsm = reg.Reg_user.email
            
            match k: 
                case 'name_reply': 
                    text = kb.text_menu['name_reply']
                    await state.set_state(fsm)
                    value = kb.menu_to_keyboard['name_reply'](await rq.get_status(tg_id))
                case 'phone_number_reply': 
                    text = kb.text_menu['phone_number_reply']
                    await state.set_state(fsm)
                    value = kb.menu_to_keyboard['phone_number_reply']()


            await message.answer(text=text, reply_markup=value)
            

        else: 

            e = await rq.change_list_steps(tg_id=tg_id, parametrs=None, my_list='back', action=None, is_exists=True, arr_index=-1)
            k = e[0] if e else []
            match k:
                case 'menu': 
                    text = kb.text_menu['menu']
                    value = kb.menu_to_keyboard['menu'](status) 
                case 'admin_menu': 
                    text = kb.text_menu['admin_menu']
                    value = kb.menu_to_keyboard['admin_menu'](admin_exists)   
                     
            await message.answer(text=text, reply_markup=value)
            
    
    elif await rq.change_list_steps(tg_id=tg_id, parametrs=None, my_list='callback_back', action=None, is_exists=True):
            data = {}
            if state is not None: data = await state.get_data() 
            name = data.get('change_name') if data.get('change_name') is not None else data.get('name')
            phone_number = data.get('change_phone_number') if data.get('change_phone_number') is not None else data.get('phone_number')
            email = data.get('change_email') if data.get('change_email') is not None else data.get('email')
            status = await rq.get_status(message.from_user.id)
            await message.answer(text=(
            f'Name: {name}\n'
            f'Phone number: {phone_number}\n'
            f'Email: {email}'
            ), reply_markup=kb.menu_to_keyboard['registration_end']() if status == 'admin' else kb.menu_to_keyboard['registration_user_end']())
            
    

    else:
        main_queue = await rq.change_list_steps(tg_id=tg_id, parametrs=None, my_list='back', action=None, is_exists=True)
        if main_queue and len(main_queue) > 1:
            await rq.change_list_steps(tg_id=tg_id, parametrs=None, my_list='back', action='pop')

        e = await rq.change_list_steps(tg_id=tg_id, parametrs=None, my_list='back', action=None, is_exists=True, arr_index=-1)
        k = e[0] if e else []
        match k: 
            case 'menu': 
                text = kb.text_menu['menu']
                value = kb.menu_to_keyboard['menu'](status)  
            case 'admin_menu': 
                text = kb.text_menu['admin_menu']
                value = kb.menu_to_keyboard['admin_menu'](admin_exists)
    

        await message.answer(text=text, reply_markup=value)

    
@rt.message(CommandStart())
async def start(message: Message, state: FSMContext):
    await rq.state_user_data(tg_id=message.from_user.id)
    await message.answer(text='📝 Реєстрація обов’язкова для користування ботом. Натисніть кнопку нижче, щоб зареєструватися.',
    reply_markup= kb.menu_to_keyboard['start']())
    
     


@rt.message(Command('admin_menu'))
async def admin_menu(message: Message, state: FSMContext):
    
    admin_exists = await rq.admin_is_created()
    menu = kb.menu_to_keyboard['admin_menu'](admin_exists)
    await rq.change_list_steps(tg_id=message.from_user.id, parametrs=['admin_menu'], my_list='back', action='append')
    await message.answer(text='Ви перейшли в меню адміністратора!', reply_markup= menu)

@rt.message(F.text == 'Назад🔙')
async def back_reply(message: Message, state: FSMContext):
    await back(message, state=state)

@rt.callback_query(F.data == 'back')
async def back_inline(callback: CallbackQuery, state: FSMContext):
    tg_id = callback.from_user.id
    status = await rq.get_status(tg_id)
    if status == 'user':
        await callback.message.edit_reply_markup(reply_markup=kb.menu_to_keyboard['registration_user_end']())
    else:
        await callback.message.edit_reply_markup(reply_markup=kb.menu_to_keyboard['registration_admin_end']())


@rt.message(F.text == 'Мій профіль')
async def show_data(message: Message, state: FSMContext):
    data = await rq.get_registration_data(tg_id=message.from_user.id)
    if data is not None:
        await message.answer(text=(
        'Профіль 👤\n'
        f'Name: {data['name']}\n'
        f'Phone number: {data['phone_number']}\n'
        f'Email: {data['email']}\n'
        ), reply_markup=kb.menu_to_keyboard['change_data']())
    else:
        await message.answer(text='Ви не зареєстровані!')

@rt.callback_query(F.data == 'change_data')
async def change_data(callback: CallbackQuery, state: FSMContext):
    status = 'change_data_user' if await rq.get_status(callback.from_user.id) == 'user' else 'change_data_admin'
    await callback.message.edit_reply_markup(reply_markup=kb.menu_to_keyboard[status]())


@rt.message(F.text == 'Контакти')
async def show_contacts(message: Message, state: FSMContext):
    data = await rq.get_registration_data(tg_id=message.from_user.id)
    if data is not None:
        await message.answer(text=(
        'Контакти 📞\n'
        f'Phone number: {data['phone_number']}\n'
        f'Email: {data['email']}\n'
        ))
    else:
        await message.answer(text='Контакти не вказані!')
    
@rt.message(F.text == 'Записатись')
async def record(message: Message, state: FSMContext):
    await message.answer(text='Переходимо на сторінку запису!', )


@rt.message(lambda msg: msg.web_app_data is not None)
async def date(message: Message, state: FSMContext):
    data = json.loads(message.web_app_data.data)
    selected_date = data['date']
    await rq.fetch_record_date_to_db(message.from_user.id, selected_date)
    await message.answer(text=f'Вас записано на {selected_date}')

@rt.callback_query(F.data == 'get')
async def get_record_data_for_admin(callback: CallbackQuery, state: FSMContext):
    recipient = await rq.get_admin()
    await send_email(recipient, 'bot.notifications000@gmail.com')
    await callback.answer(text='Дані відправлено')
    await callback.message.answer(text='Дані відправлено', reply_markup= kb.menu_to_keyboard['menu'](await rq.get_status(callback.from_user.id)))
    

async def send_email(recipient, from_: str):
    
    mess = EmailMessage()
    mess['from'] = from_
    mess['To'] = recipient['email'] 
    mess['Subject'] = 'Записи на послугу'
    mess.set_content(await rq.get_record_date())

    await aiosmtplib.send(
        mess,
        hostname='smtp.gmail.com',
        port=465,
        username=from_,
        password='kbkb ezqa sgpu sajq',
        use_tls=True,
        )




    