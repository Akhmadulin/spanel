import logging
import requests
from telegram import Update
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext

# Вставьте сюда токен вашего бота
TOKEN = 'YOUR_TELEGRAM_BOT_TOKEN'

# Уровень логирования
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)

# Функция для обработки команды /start
def start(update: Update, _: CallbackContext) -> None:
    update.message.reply_text("Привет! Я бот для проверки доступности доменов. Просто отправь мне доменное имя, и я проверю, свободно ли оно.")

# Функция для обработки текстовых сообщений
def check_domain(update: Update, _: CallbackContext) -> None:
    domain_name = update.message.text.strip()
    availability = check_domain_availability(domain_name)
    response = f"Домен '{domain_name}' {'свободен' if availability else 'занят'}."
    update.message.reply_text(response)

# Функция для проверки доступности домена
def check_domain_availability(domain_name: str) -> bool:
    try:
        # Используем API одного из сервисов для проверки доступности домена
        api_url = f"https://api.domainsdb.info/v1/domains/search?domain={domain_name}"
        response = requests.get(api_url)
        data = response.json()
        return not data['domains']
    except Exception as e:
        logging.error(f"Ошибка при проверке домена: {e}")
        return False

def main() -> None:
    updater = Updater(TOKEN)
    dispatcher = updater.dispatcher

    # Обработчик команды /start
    dispatcher.add_handler(CommandHandler("start", start))

    # Обработчик текстовых сообщений
    dispatcher.add_handler(MessageHandler(Filters.text & ~Filters.command, check_domain))

    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()

