import subprocess
import os

def install_mysql():
    try:
        # Обновление списка пакетов и установка MySQL
        subprocess.run(["sudo", "apt", "update"])
        subprocess.run(["sudo", "apt", "install", "mysql-server", "-y"])

        # Сохранение пароля MySQL в файл
        password = "A5392420t"  # Замените на свой пароль
        with open("mysql_password.txt", "w") as f:
            f.write(password)

        # Запуск MySQL и добавление автозапуска
        subprocess.run(["sudo", "systemctl", "start", "mysql"])
        subprocess.run(["sudo", "systemctl", "enable", "mysql"])

        # Настройка безопасности MySQL (простой вариант без команды mysql_secure_installation)
        subprocess.run(f"sudo mysql -e \"ALTER USER 'root'@'localhost' IDENTIFIED WITH mysql_native_password BY '{password}';\"")

        print("MySQL успешно установлен и настроен. Пароль сохранен в файл 'mysql_password.txt'")
    except Exception as e:
        print("Ошибка при установке MySQL:", e)

if __name__ == "__main__":
    install_mysql()
