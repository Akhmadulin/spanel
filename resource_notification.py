import psutil
import requests
import time

# Замените YOUR_BOT_TOKEN на токен вашего телеграм-бота
BOT_TOKEN = "6552760294:AAHHB5qJuSjGFdFZnt1F65ivG4aEB1o8U1A"
CHAT_ID = "1053452769"  # Замените на ID вашего телеграм-чата или пользователя

def send_message(message):
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    params = {
        "chat_id": CHAT_ID,
        "text": message
    }
    requests.post(url, params=params)

def get_uptime():
    with open('/proc/uptime', 'r') as f:
        uptime_seconds = float(f.readline().split()[0])
        uptime_minutes = uptime_seconds / 60
        return uptime_minutes

def check_resource_usage():
    while True:
        # Мониторинг загрузки CPU
        cpu_usage = psutil.cpu_percent(interval=1)
        if cpu_usage > 70:
            send_message(f"Внимание! Загрузка CPU превышает 70%: {cpu_usage}%")
        if cpu_usage > 80:
            send_message(f"Внимание! Загрузка CPU превышает 80%: {cpu_usage}%")
        if cpu_usage > 90:
            send_message(f"Внимание! Загрузка CPU превышает 90%: {cpu_usage}%")
        if cpu_usage == 100:
            send_message(f"Критическое состояние! Загрузка CPU достигла 100%: {cpu_usage}%")

        # Мониторинг использования памяти
        memory_usage = psutil.virtual_memory().percent
        if memory_usage > 70:
            send_message(f"Внимание! Использование памяти превышает 70%: {memory_usage}%")
        if memory_usage > 80:
            send_message(f"Внимание! Использование памяти превышает 80%: {memory_usage}%")
        if memory_usage > 90:
            send_message(f"Внимание! Использование памяти превышает 90%: {memory_usage}%")
        if memory_usage == 100:
            send_message(f"Критическое состояние! Использование памяти достигло 100%: {memory_usage}%")

        # Мониторинг использования swap
        swap_usage = psutil.swap_memory().percent
        if swap_usage > 70:
            send_message(f"Внимание! Использование swap превышает 70%: {swap_usage}%")
        if swap_usage > 80:
            send_message(f"Внимание! Использование swap превышает 80%: {swap_usage}%")
        if swap_usage > 90:
            send_message(f"Внимание! Использование swap превышает 90%: {swap_usage}%")
        if swap_usage == 100:
            send_message(f"Критическое состояние! Использование swap достигло 100%: {swap_usage}%")

        # Мониторинг использования жесткого диска
        disk_usage = psutil.disk_usage('/').percent
        if disk_usage > 70:
            send_message(f"Внимание! Использование места на жестком диске превышает 70%: {disk_usage}%")
        if disk_usage > 80:
            send_message(f"Внимание! Использование места на жестком диске превышает 80%: {disk_usage}%")
        if disk_usage > 90:
            send_message(f"Внимание! Использование места на жестком диске превышает 90%: {disk_usage}%")
        if disk_usage == 100:
            send_message(f"Критическое состояние! Использование места на жестком диске достигло 100%: {disk_usage}%")

        # Отправка уведомления при загрузке сервера
        uptime_minutes = get_uptime()
        if uptime_minutes < 2:
            send_message("Сервер был перезагружен.")

        time.sleep(60)  # Проверка каждые 60 секунд

if __name__ == "__main__":
    check_resource_usage()
