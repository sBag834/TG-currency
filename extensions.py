import telebot

from cfg import token, API_URL
from utils import Get

bot = telebot.TeleBot(token)

@bot.message_handler(commands=['start', 'help'])
def welcome(message):
    bot.reply_to(message, "Чтобы начать работу, отправьте сообщение боту в следующем формате:\n"
                          "{валюта} {в какую валюту вы хотите перевести} {количество первой валюты}\n"
                          "\n"
                          "Что бы получить список доступных валют, напиши /values")

@bot.message_handler(commands=['values'])
def values(message):
    bot.reply_to(message, "USD - доллары\n"
                          "EUR - евро\n"
                          "RUB - рубли\n"
                          "UAH - гривны")

@bot.message_handler(func=lambda message: True)
def handle_message(message):
    try:
        parts = message.text.split()

        if len(parts) != 3:
            bot.reply_to(message, "Неправильный формат сообщения!!!\n"
                         "Используйте формат: <валюта_источник> <валюта_назначение> <количество>\n"
                         "Пример: UDS RUB 100")
            return

        base = parts[0].upper()   # Первая валюта
        quote = parts[1].upper()  # Вторая валюта
        amount = float(parts[2])  # Количество

        if base == quote:
            bot.reply_to(message, f'Нельзя переводить одинаковые валюты {quote}.')
            return

        if amount <= 0:
            bot.reply_to(message, 'Количество валюты не может быть меньше нуля.')
            return

        rate = Get.get_price(base, quote)

        if rate is None:
            bot.reply_to(message, "Не удалось получить курс валют. Проверьте правильность введенных валют или попробуйте позже.")
            return

        converted_amount = rate * amount

        response = f"{amount} {base} = {converted_amount:.2f} {quote} по текущему курсу."
        bot.reply_to(message, response)

    except Exception as e:
        bot.reply_to(message, f"Произошла ошибка: {str(e)}")

bot.polling(none_stop=True)