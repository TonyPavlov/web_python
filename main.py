import telebot
import requests
import json

bot = telebot.TeleBot("6799321545:AAE-JQIYV5Ob5sGsPXM8T8dt9xHox7qMnyM")
API_weather = "8a2c100e0c5ab358a826f7ca1395ef69"

@bot.message_handler(commands=['start'])
def main(message):
    bot.send_message(message.chat.id, f'Привіт, {message.from_user.first_name} {message.from_user.last_name}! Ррадий тебе бачити! '
                                      f'Якщо ти хочеш дізнатись про поточну погоду, то напиши назву міста. \n'
                                      f'PS: При введені міста, підримує латинські та кирилиці символи')


@bot.message_handler(content_types=['text'])
def get_weather(message):

    city = message.text.strip().lower()
    res = requests.get(f'https://api.openweathermap.org/data/2.5/weather?q={city}&appid={API_weather}&units=metric')
    if res.status_code == 200:
        data = json.loads(res.text)
        bot.reply_to(message,
                 f'Погода на поточному часі - {city}\n'
                 f'Погода: {data["weather"]}\n'
                 f'Температура: {data["main"]["temp"]} С°\n'
                 f'Вологість: {data["main"]["humidity"]}%\n'
                 f'Тиск: {data["main"]["pressure"]} мм.рт.ст.\n'
                 f'Вітер: {data["wind"]["speed"]} м/c'
                 )
        image = 'icon_sun.png' if data["main"]["temp"] > 10.0 else 'icon_sun_cloudy.png'

        file = open('./' + image, 'rb')
        bot.send_photo(message.chat.id, file)
    else:
        bot.reply_to(message, 'Такого міста світу ще поки що не існує, спробуйте інше місто')

bot.polling(none_stop=True)