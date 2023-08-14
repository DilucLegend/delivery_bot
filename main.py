import database
import buttons

from geopy.geocoders import Nominatim
import telebot
from telebot.types import ReplyKeyboardRemove

# Sozdayom podklyuchenie k botu
bot = telebot.TeleBot('6254725887:AAHgYD1JuSSNlFwgrGc_w1q49elDFy_aSkw')

geolocator = Nominatim(user_agent='Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/113.0.0.0 Safari/537.36')

# Slovar dlya vremennix dannix
users = {}

# database.add_product_to_cart('Yabloko', 12, 12000, 'Krasniy', 'https://www.google.com/url?sa=i&url=https%3A%2F%2Fwww.healthline.com%2Fnutrition%2F10-health-benefits-of-apples&psig=AOvVaw21JGwYtxy1Hdvg4BTr3Ejr&ust=1685200029328000&source=images&cd=vfe&ved=0CBEQjRxqFwoTCMjayryhk_8CFQAAAAAdAAAAABAE')

@bot.message_handler(commands=['start'])
def strat_message(message):
    # poluchim telegram aydi
    user_id = message.from_user.id

    print(user_id)
    # proverka polzovatelya
    checker = database.check_user(user_id)

    # yesli polzovatel yest v baze
    if checker:
        # poluchim aktualniy spisok produktov
        products = database.get_pr_name_id()
        # otpravim coobshenie s menyu
        bot.send_message(user_id, 'Привет', reply_markup=ReplyKeyboardRemove())
        bot.send_message(user_id, 'Выберите пункт:', reply_markup=buttons.main_menu_kb(products))

    # yesli net polzovatelya v baze
    elif not checker:
        bot.send_message(user_id, 'Привет \nОтправь своё имя')

        # perehod na poluchenie imeni
        bot.register_next_step_handler(message, get_name)

# Этап получение имени
def get_name(message,):
    # Получим telegram id текущего ползователя(кто общается с ботом)
    user_id = message.from_user.id
    name = message.text
    bot.send_message(user_id,'Отправьте номер!',reply_markup=buttons.phone_number())
    bot.register_next_step_handler(message, get_number, name)


# Этап получение номера телефона
def get_number(message, name):
    user_id = message.from_user.id
    if message.contact:
        phone_number = message.contact.phone_number
        database.register_user(user_id, name, phone_number, 'Not yet')

        products = database.get_pr_name_id()

        bot.send_message(user_id, 'Привет', reply_markup=ReplyKeyboardRemove())
        bot.send_message(user_id, 'Меню',reply_markup=buttons.main_menu_kb(products))

        bot.register_next_step_handler(message, get_number, name)
    else:
        bot.send_message(user_id, 'Отправтье номер через кнопки')
        bot.register_next_step_handler(message,get_number, name)

# Obrabotchik knopok (Oformit, zakaz, korzina)
@bot.callback_query_handler(lambda call: call.data in ['order', 'cart', 'clear cart'])
def main_menu_handle(call):
    user_id = call.message.chat.id
    message_id = call.message.message_id

    # Yesli najal na knopku: ofrmit zakaz
    if call.data == 'order':
        # Udalim soobsheniya s verhnimi knopkami
        bot.delete_message(user_id, message_id)
        # pomenyayem tekst na 'Otpravte lokatsiyu
        bot.send_message(user_id, 'Отправьте локацию', reply_markup=buttons.location_kb())

        bot.register_next_step_handler(call.message, get_location)

    # Yesli najal na knopku korzina
    elif call.data == 'cart':
        # zapros podtverjdeniya zakaza
        user_cart = database.get_exact_user_cart(user_id)

        # formiruyem soobshenie so vsemi dannii
        full_text = 'Ваше корзина:\n\n'
        total_amount = 0

        for i in user_cart:
            full_text += f'{i[0]} x {i[1]} = {i[2]}\n'
            total_amount += i[1]

        # itog i adres
        full_text += f'\nИтог: {total_amount}'
        bot.edit_message_text(full_text,user_id, message_id, reply_markup=buttons.get_cart_kb())

    # Yesli najal na ochistit korzinu
    elif call.data == 'clear cart':
        # Vizov funktsii
        database.delete_product_from_cart(user_id)

        bot.edit_message_text('Ваша корзина очищена!', user_id, message_id, reply_markup=buttons.main_menu_kb(database.get_pr_name_id()))
def get_location(message):
    user_id = message.from_user.id
    # Otpravil li lokatsiyu
    if message.location:
        # sohranim dolgotu i shirotu
        latitude = message.location.latitude
        longitude = message.location.longitude

        # preobrazuyem koordinati na normalniy adress
        address = 'geolocator.reverse((latitude,longitude)).address'

        # zapros podtverjdeniya zakaza
        user_cart = database.get_exact_user_cart(user_id)

        # formiruyem soobshenie so vsemi dannimi
        full_text = 'Ваш заказ:\n\n'
        user_info = database.get_user_number_name(user_id)
        full_text += f'Имя: {user_info[0]}\nНомер телефона: {user_info[1]}\n\n'
        total_amount = 0

        for i in user_cart:
            full_text += f'{i[0]} x {i[1]} = {i[2]}\n'
            total_amount += i[1]

        # itog i adres
        full_text += f'\nИтог: {total_amount}\nАдрес:{address}'

        bot.send_message(user_id, full_text, reply_markup=buttons.get_accept())
        #perehod na etap podtverjdeniya
        bot.register_next_step_handler(message,get_accept, address, full_text)

# funksiya sohraneniya statusa
def get_accept(message, address, full_text):
    user_id = message.from_user.id
    message_id = message.message_id
    message_text = message.text
    products = database.get_pr_name_id()

    if message_text == 'Подтвердить':
        # ochistit korzinu
        database.delete_product_from_cart(user_id)

        # otpravim adminu soobshenie o novom zakaze
        bot.send_message(1067162504, full_text.replace('Ваш', 'Новый'))

        bot.send_message(user_id, 'Заказ оформлен!', reply_markup=ReplyKeyboardRemove())
        bot.send_message(user_id, 'Ваш заказ обрабатывается \nЖдите звонка', reply_markup=buttons.main_menu_kb(products))

    elif message_text == 'Отменить':
        bot.delete_message(user_id, message_id)
        bot.send_message(user_id, 'Заказ не оформлен!', reply_markup=ReplyKeyboardRemove())
        bot.send_message(user_id, 'Выберите пункт меню', reply_markup=buttons.main_menu_kb(products))


# Obrabotchik vibora kolichestva
@bot.callback_query_handler(lambda call: call.data in ['increment', 'decrement', 'to cart', 'back'])
def get_user_product_count(call):
    # Sohranim aydi polzovatelya
    user_id = call.message.chat.id

    # Yesli polzovatel najal na +
    if call.data == 'increment':
        actual_count = users[user_id]['pr_count']
        users[user_id]['pr_count']+=1

        # Menyayem znachenie knopki
        bot.edit_message_reply_markup(chat_id=user_id,message_id=call.message.message_id,
                                      reply_markup=buttons.choose_product_count('increment', actual_count))

    # decrement
    elif call.data == 'decrement':
        actual_count = users[user_id]['pr_count']
        users[user_id]['pr_count'] -= 1

        # Menyayem znachenie knopki
        bot.edit_message_reply_markup(chat_id=user_id, message_id=call.message.message_id,
                                      reply_markup=buttons.choose_product_count('decrement', actual_count))

    elif call.data == 'back':
        # poluchim telegram aydi
        user_id = call.from_user.id

        message_id = call.message.message_id
        bot.delete_message(user_id, message_id)

        # poluchim aktualniy spisok produktov
        products = database.get_pr_name_id()
        # otpravim coobshenie s menyu
        bot.send_message(user_id, 'Выберите пункт:', reply_markup=buttons.main_menu_kb(products))

    elif call.data == 'to cart':
        #Poluchim dannie
        product_count = users[user_id]['pr_count']
        user_product = users[user_id]['pr_name']

        # Dobavlyaem v bazu(v korzinu polzovatelya)
        database.add_product_to_cart(user_id, user_product, product_count)

        # Poluchayem obratno menyu
        products = database.get_pr_name_id()
        # menyayem na menyu
        bot.edit_message_text('Продукты добавлены в корзину \nЧто нибудь ещё?', user_id, call.message.message_id, reply_markup=buttons.main_menu_kb(products))

    # back (bot.edit_message_text -> reply_mark_up=buttons.main_menu_kb(products)
# Obrabotchik vibora tovara
@bot.callback_query_handler(lambda call: int(call.data) in database.get_pr_id())
def get_user_product(call):
    # sohronyayem aydi polzovatelya
    user_id = call.message.chat.id

    # Sohranim produkt vo vremenniy slovar
    # call.data - znachenie najatoy knopki
    users[user_id] = {'pr_name': call.data, 'pr_count': 1}

    # sohronyayem aydi soobsheniya
    message_id = call.message.message_id
    bot.edit_message_text('Выберите количество', chat_id=user_id, message_id=message_id,reply_markup=buttons.choose_product_count())


bot.polling(none_stop=True)