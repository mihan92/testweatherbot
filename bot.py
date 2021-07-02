import telebot
from telebot import types
from key import TOKEN
from key import OWMTOKEN  # import from key.py
from pyowm import OWM
from pyowm.utils.config import get_default_config
import create_db

db = create_db
tb = telebot.TeleBot(TOKEN)

@tb.message_handler(commands=['start'])
def send_welcome(message):
	tb.send_message(message.chat.id, "Привет, {0.first_name}! Нужна погода? Введи название города или страны.\nНапример: Минск или Minsk".format(message.from_user))
	

@tb.message_handler(commands=['help'])
def send_welcome(message):
	tb.send_message(message.chat.id, "Я умею показывать погоду и отвечать на стикеры :)")

@tb.message_handler(content_types=['text'])
def wd_msg(message):
	markup = types.InlineKeyboardMarkup(row_width=1)
	item = types.InlineKeyboardButton('Обновить погоду', callback_data='id_1')
	#item2 = types.InlineKeyboardButton('Изменить город', callback_data='id_2')
	markup.add(item)
	try:
		city = message.text
		config_dict = get_default_config()
		config_dict['language'] = 'ru'
		owm = OWM(OWMTOKEN, config_dict )
		mgr = owm.weather_manager()

		observation = mgr.weather_at_place(city)
		w = observation.weather
		temp = w.temperature('celsius')['temp']
		temp2 = w.temperature('celsius')['feels_like']
		weather = w.detailed_status 
		humidity = w.humidity
		if -100 <= round(temp) <= -1:
			msg = 'Сидим дома и не высовываемся'
		elif 0 <= round(temp) <= 10:
			msg = 'Надевай куртку, ну его в баню'
		elif 11 <= round(temp) <= 19:
			msg = 'Ну такое себе.. В шортах особо не походишь'
		elif 20 <= round(temp) <= 100:
			msg = 'Надевай шлепки, пора на речку :)'
		text = f'В городе {city} сейчас {round(temp)} °С\nОщущается как {round(temp2)} °С\nОблачность: {weather}\nВлажность: {humidity}%\n{msg}'
		tb.send_message(message.chat.id, text, reply_markup=markup)
		db.user_add(user_id = message.from_user.id, username = message.from_user.username, firstname = message.from_user.first_name, city = message.text)

	except:
		tb.send_message(message.chat.id, 'Такой город не найден')
		print(str(message.text), ' - Не найден')

@tb.callback_query_handler(func=lambda call:True)
def callback(call):
	markup = types.InlineKeyboardMarkup(row_width=1)
	item = types.InlineKeyboardButton('Обновить погоду', callback_data='id_1')
	#item2 = types.InlineKeyboardButton('Изменить город', callback_data='id_2')
	markup.add(item)
	if call.message:
		if call.data == 'id_1':
			tb.send_message(call.message.chat.id, call.message.text, reply_markup=markup)
			tb.answer_callback_query(call.id)
		elif call.data == 'id_2':
			tb.send_message(call.message.chat.id, 'Введи название города или страны')
			tb.answer_callback_query(call.id)

@tb.message_handler(content_types=['sticker'])
def echo_stk(message):
	tb.send_sticker(message.chat.id, message.sticker.file_id)


db.create_db()
tb.polling(none_stop = True)
