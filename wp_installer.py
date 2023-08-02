import os
import requests
import tarfile

from dotenv import load_dotenv

def send_message_via_telegram(token, chat_id, message):
    url = f"https://api.telegram.org/bot{token}/sendMessage"
    data = {"chat_id": chat_id, "text": message}
    response = requests.post(url, data=data)
    return response.json()

def install_wordpress(domain):
    try:
        # Устанавливаем WordPress
        wp_download_url = "https://wordpress.org/latest.tar.gz"
        wp_tar_file = "latest.tar.gz"
        wp_directory = f"/var/www/{domain}"

        # Загружаем и распаковываем WordPress
        r = requests.get(wp_download_url)
        with open(wp_tar_file, "wb") as f:
            f.write(r.content)
        with tarfile.open(wp_tar_file, "r:gz") as tar:
            tar.extractall(path=wp_directory)
        os.remove(wp_tar_file)

        # Создаем базу данных и пользователя MySQL
        database_name = f"db_{domain}"
        db_user = f"user_{domain}"
        db_password = "your_database_password"  # Замените на свой пароль
        create_db_command = f"mysql -u root -e \"CREATE DATABASE {database_name};\""
        create_user_command = f"mysql -u root -e \"CREATE USER '{db_user}'@'localhost' IDENTIFIED BY '{db_password}';\""
        grant_privileges_command = f"mysql -u root -e \"GRANT ALL PRIVILEGES ON {database_name}.* TO '{db_user}'@'localhost';\""
        for command in [create_db_command, create_user_command, grant_privileges_command]:
            os.system(command)

        # Отправляем информацию о базе данных, логине и пароле через Telegram бота
        telegram_token = os.getenv("TELEGRAM_BOT_TOKEN")
        telegram_chat_id = os.getenv("TELEGRAM_CHAT_ID")
        message = f"Установка WordPress для домена {domain}\n\nURL: http://{domain}\nDatabase: {database_name}\nUsername: {db_user}\nPassword: {db_password}"
        send_message_via_telegram(telegram_token, telegram_chat_id, message)

        print("Установка WordPress успешно завершена.")

    except Exception as e:
        print("Произошла ошибка:", e)

if __name__ == "__main__":
    load_dotenv()
    domain = "example.com"  # Замените на ваш домен
    install_wordpress(domain)
