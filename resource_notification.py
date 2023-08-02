import psutil
import requests
import time

# Замените YOUR_BOT_TOKEN на токен вашего телеграм-бота
BOT_TOKEN = "6552760294:AAHHB5qJuSjGFdFZnt1F65ivG4aEB1o8U1A"
CHAT_ID = "1053452769"  # Замените на ID вашего телеграм-чата или пользователя

# Переменные для хранения предыдущих значений нагрузки
previous_cpu_usage = None
previous_memory_usage = None
previous_swap_usage = None
previous_disk_usage = None

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
    global previous_cpu_usage, previous_memory_usage, previous_swap_usage, previous_disk_usage

    while True:
        # Мониторинг загрузки CPU
        cpu_usage = psutil.cpu_percent(interval=1)
        if previous_cpu_usage is not None and cpu_usage < previous_cpu_usage:
            send_message(f"Внимание! Загрузка CPU снизилась до {cpu_usage}%")
        previous_cpu_usage = cpu_usage

        # Мониторинг использования памяти
        memory_usage = psutil.virtual_memory().percent
        if previous_memory_usage is not None and memory_usage < previous_memory_usage:
            send_message(f"Внимание! Использование памяти снизилось до {memory_usage}%")
        previous_memory_usage = memory_usage

        # Мониторинг использования swap
        swap_usage = psutil.swap_memory().percent
        if previous_swap_usage is not None and swap_usage < previous_swap_usage:
            send_message(f"Внимание! Использование swap снизилось до {swap_usage}%")
        previous_swap_usage = swap_usage

        # Мониторинг использования жесткого диска
        disk_usage = psutil.disk_usage('/').percent
        if previous_disk_usage is not None and disk_usage < previous_disk_usage:
            send_message(f"Внимание! Использование места на жестком диске снизилось до {disk_usage}%")
        previous_disk_usage = disk_usage

        # Отправка уведомления при загрузке сервера
        uptime_minutes = get_uptime()
        if uptime_minutes < 1:
            send_message("Сервер был перезагружен.")

        time.sleep(60)  # Проверка каждые 60 секунд

if __name__ == "__main__":
    check_resource_usage()
