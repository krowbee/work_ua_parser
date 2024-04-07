import telebot
from parse import main

BOT_API_TOKEN = ''

bot = telebot.TeleBot(BOT_API_TOKEN)


@bot.message_handler(commands=['start'])
def greeting(message):
    bot.send_message(message.chat.id, 'Привіт, напиши назву посади,\n і я надішлю тобі останні виставлені вакансії')

@bot.message_handler(func=lambda message:True)
def send_vacancy(message):
    bot.send_message(message.chat.id,'Збираю інформацію по останніх вакансіях...')

    data = main(str(message.text))

    counter = 1
    if data == False:
        bot.send_message(message.chat.id,'Вакансій не знайдено!')
    else:    
        for key,value in data.items():
            info = data[key]
            bot.send_message(message.chat.id,f"Назва вакансії: \n {info['name']}\n")
            if len(info['requirements']) != 0:
                bot.send_message(message.chat.id,f"Вимоги до вакансії:\n\n") 
                bot.send_message(message.chat.id,f" ".join(info['requirements']))
            bot.send_message(message.chat.id,f"Опис: \n {info['description']} \n \n Посилання на вакансію: {info['job_url']}")
            counter +=1
    data.clear()    

if __name__ == '__main__':
    bot.polling(none_stop=True)