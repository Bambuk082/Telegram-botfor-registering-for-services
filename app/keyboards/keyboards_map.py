import app.keyboards.keyboards as kb

menu_to_keyboard = {
    'start': kb.start_kb,
    'menu': kb.menu,
    'admin_menu': kb.admin_menu,

    'change_data': kb.change_data,
    'change_data_admin': kb.change_data_admin,
    'change_data_user': kb.change_data_user,

    'registration_admin_end': kb.registration_admin_end,
    'registration_user_end': kb.registration_user_end,

    'name_reply': kb.Reg_menu().name_reply,
    'phone_number_reply': kb.Reg_menu().phone_number_reply,
    'email_reply': kb.Reg_menu().email_reply,
    # Клавіатура для зміни даних реєстрації
    'change_name': kb.Reg_menu().change_name_reply,
    'change_phone_number': kb.Reg_menu().change_phone_number_reply,
    'change_email': kb.Reg_menu().change_email_reply,

    
}
text_menu = {
    'start': '',
    'menu': 'Ви в головному меню!',
    'admin_menu': 'Ви в меню адміністратора!',
    'name_reply': 'Введіть нове ім’я!',
    'phone_number_reply': 'Введіть новий номер телефону!',
    'change_email': 'Введіть нову електронну пошту'

}