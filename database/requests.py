from database.db import async_session
from database.models import User
from sqlalchemy import select, or_



# Отримання статусу користувача
async def get_status(tg_id: int):
    async with async_session() as session:
        user = await session.scalar(select(User).where(User.tg_id == tg_id))
        return user.status

# Запис користувача в бд
async def state_user_data(tg_id: int):
    async with async_session() as session:
        user= await session.scalar(select(User).where(User.tg_id == tg_id))

        if not user:
            session.add(User(tg_id = tg_id))
            await session.commit()

# Перевірка наявності адміна
async def admin_is_created():
    async with async_session() as session:
        admin_exists = await session.scalar(select(User).where(User.is_admin == True))
        return True if admin_exists else False
    
# Дістаємо дані адміна
async def get_admin():
    async with async_session() as session:
        admin_exists = await session.scalar(select(User).where(User.is_admin == True))
        return admin_exists.registration_data

#  Збереження даних в базу даних
async def save_data_to_db(data: dict, tg_id: int, is_admin: bool):
    async with async_session() as session:
        result = await session.execute(select(User).where(User.tg_id == tg_id))
        user = result.scalar_one_or_none()
        if user:
            user.status = 'admin' if is_admin else 'user'
            user.registration_data = data
            user.is_admin = True if is_admin else False
            user.phone_number = data['phone_number']
            user.first_name = data['name']
        else:
            user = User(
                tg_id = tg_id,
                status = 'admin' if is_admin else 'user',
                registration_data = data,
                is_admin = True if is_admin else False
                )
            session.add(user)
        session.add(user)
        await session.commit()


# Функція яка може повертати потрібний список з користувача та змінювати його і при потребі повертати потрібний елемент
async def change_list_steps(tg_id, parametrs, my_list, action, is_exists=False, index=None, arr_index=None):
    async with async_session() as session:
        user = await session.scalar(select(User).where(User.tg_id == tg_id))
        
        

        if user:
            arr = []
            match my_list:
                case 'back': arr = list(user.queue_message_to_back)
                case 'registration_back': arr = list(user.queue_registration_to_back) 
                case 'callback_back': arr = list(user.queue_callback_registration_to_back)
                case 'change_data': arr = list(user.change_data)
                case _: return 
            if action == 'append':
                arr.append(parametrs)
            elif action == 'clear':
                arr.clear()
            elif action == 'pop'and arr:
                arr.pop(index if index is not None else -1)
            match my_list:
                case 'back': user.queue_message_to_back = arr
                case 'registration_back': user.queue_registration_to_back = arr
                case 'callback_back': user.queue_callback_registration_to_back = arr
                case 'change_data': user.change_data = arr
                case _: return


            if is_exists:
                match my_list:
                    case 'back': return user.queue_message_to_back if arr_index is None else user.queue_message_to_back[arr_index]
                    case 'registration_back': return user.queue_registration_to_back if arr_index is None else user.queue_registration_to_back[arr_index]
                    case 'callback_back': return user.queue_callback_registration_to_back if arr_index is None else user.queue_callback_registration_to_back[arr_index]
                    case 'change_data': return user.change_data if arr_index is None else user.change_data[arr_index]
                    case _: return
        else:
            return None
        
        
        await session.commit()

# Отримання даних реєстрації
async def get_registration_data(tg_id):
    async with async_session() as session:
        user = await session.scalar(select(User).where(User.tg_id == tg_id))

        if user: 
            return user.registration_data
        
# Зміна даних реєстрації        
async def change_registratio_data(tg_id, value, parametrs):
    async with async_session() as session:
        result = await session.execute(select(User).where(User.tg_id == tg_id))
        user = result.scalar_one()

        if user:
           user.registration_data[parametrs] = value


# Добавлення в бд дати запису 
async def fetch_record_date_to_db(tg_id, data):
    async with async_session() as session:
       user = await session.scalar(select(User).where(User.tg_id == tg_id))

       if user:
           user.record_date = data
           await session.commit()

# Отримання всіх саписів з бд
async def get_record_date():
    async with async_session() as session:
        user_data = await session.scalars(select(User).where(User.record_date != None))
        user_data  = user_data.all()
        
        records = [
            f'''
        name: {u.first_name}
        phone: {u.phone_number}
        record date: {u.record_date}
        '''
        for u in user_data

        ]

    if user_data:
        return '\n'.join(records)
    
async def re_register_admin(tg_id):
    async with async_session() as session:
        admin = await session.scalar(select(User).where(User.is_admin == True))
        user = await session.scalar(select(User).where(User.tg_id == tg_id))

        if admin and user:
            admin.is_admin = False
            admin.status = 'user'
            user.is_admin = True
            user.status = 'admin'            
            await session.commit()
        else:
            return

