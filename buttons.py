from telebot.types import InlineKeyboardButton, InlineKeyboardMarkup, ReplyKeyboardMarkup, KeyboardButton


# Knopki so vsemi produktami(osnovnoe menyu)
def main_menu_kb(products_from_database):
    # sozdayom prostranstvo
    kb = InlineKeyboardMarkup(row_width=2)

    # sozdayom knopki(nesgorayimmie)
    order = InlineKeyboardButton(text='Оформить заказ', callback_data='order')
    cart = InlineKeyboardButton(text='Корзина', callback_data='cart')

    # generatsiya knopok

    # sozdayom knopki s produktami
    all_products = [InlineKeyboardButton(text=i[0], callback_data=i[1]) for i in products_from_database]

    # obyedenit prostranstvo knopkami
    kb.row(order)
    kb.add(*all_products)
    kb.row(cart)

    return kb

# knopki dlya vibora kolichestva
def choose_product_count(plus_or_minus = '', current_amount=1):
    # Sozdayom prostranstvo dlya knopok
    kb = InlineKeyboardMarkup(row_width=3)

    # Nesgorayemaya knopka
    back = InlineKeyboardButton(text='Назад', callback_data='back')
    plus = InlineKeyboardButton(text='+', callback_data='increment')
    minus = InlineKeyboardButton(text='-', callback_data='decrement')
    count = InlineKeyboardButton(text=str(current_amount), callback_data=str(current_amount))
    add_to_cart = InlineKeyboardButton('Добавить в корзину', callback_data='to cart')


    # sozdayom sami knopki +/-
    if plus_or_minus == 'increment':
        new_amount = int(current_amount)+1
        count = InlineKeyboardButton(text=str(new_amount),callback_data=str(new_amount))
    elif plus_or_minus == 'decrement':
        if int(current_amount) !=1:
            new_amount = int(current_amount)+1
            count = InlineKeyboardButton(text=str(new_amount),callback_data=str(new_amount))

    # Obyedenim knopki s prostranstvom
    kb.add(minus, count, plus)
    kb.row(add_to_cart)
    kb.row(back)

    # Vozvrashayem knopki
    return kb

# knopki dlya otpravki nomera telefona
def phone_number():
    kb = ReplyKeyboardMarkup(resize_keyboard=True)

    number = KeyboardButton('Поделиться контактом', request_contact=True)
    kb.add(number)

    return kb

def location_kb():
    kb = ReplyKeyboardMarkup(resize_keyboard=True)

    location = KeyboardButton('Поделиться локацией', request_location=True)
    kb.add(location)

    return kb

# knopki dlya podtverjdeniya zakaza
def get_accept():
    kb = ReplyKeyboardMarkup(resize_keyboard=True)

    yes = KeyboardButton('Подтвердить')
    no = KeyboardButton('Отменить')

    kb.add(yes, no)

    return kb

# knopki pri perehode v korzinu
def get_cart_kb():
    kb = InlineKeyboardMarkup(row_width=1)

    clear_cart = InlineKeyboardButton('Очистить корзину', callback_data='clear cart')
    order = InlineKeyboardButton('Оформить заказ', callback_data='order')
    back = InlineKeyboardButton('Назад', callback_data='back')

    kb.add(clear_cart, order, back)

    return kb