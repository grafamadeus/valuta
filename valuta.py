from bs4 import BeautifulSoup as Bs
import requests
import telebot
from telebot import types
from config import TOKEN


    
def dollar(valuta, num):
    r = requests.get('https://www.optimabank.kg/index.php?option=com_nbrates&view=default&Itemid=196&lang=ru')
    soup = Bs(r.text,'html.parser')
    items = soup.find('div',class_=f'iso-{valuta} row{num}')
    new_list = []
    new_list.append({
        'покупка': items.find('div',class_='rate buy').find('span').get_text(strip = True),
        'продажа': items.find('div',class_='rate sell').find('span').get_text(strip = True),
    })

    result = []
    
    for i in new_list:
        for key, value in i.items():
            result.append(f"{key}: {value}")

    finish = '\n'.join(result)
    
    return finish


bot = telebot.TeleBot(TOKEN)


menu = types.ReplyKeyboardMarkup(resize_keyboard=True)
menu.row("USD")
menu.row("EUR")
menu.row("KZT")
menu.row("RUB")


@bot.message_handler(commands=['start'])

def start(message):
    bot.send_message(message.chat.id,"выберите валюту чтобы увидеть актуальную цену", reply_markup=menu)



@bot.message_handler(func=lambda message:True)
def second(message):
    if message.text == "USD":
        bot.send_message(message.chat.id,dollar('USD',0))
    elif message.text == "EUR":
        bot.send_message(message.chat.id,dollar('EUR',1))
    elif message.text == "KZT":
        bot.send_message(message.chat.id,dollar('KZT',0))
    elif message.text == "RUB":
        bot.send_message(message.chat.id,dollar('RUB',1))
    else:
        bot.send_message(message.chat.id, "ТЫ ГЕЙ")
        return
        


bot.polling(non_stop=True)