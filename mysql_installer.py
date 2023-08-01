import subprocess
import os

def install_mysql():
    try:
        # Обновление списка пакетов и установка MySQL
        subprocess.run(["sudo", "apt", "update"])
        subprocess.run(["sudo", "apt", "install", "mysql-server", "-y"])

        # Сохранение пароля MySQL в файл
        password = "YOUR_MYSQL_PASSWORD"  # Замените на свой пароль
        with open("mysql_password.txt", "w") as f:
            f.write(password)

        # Запуск MySQL и добавление автозапуска
        subprocess.run(["sudo", "systemctl", "start", "mysql"])
        subprocess.run(["sudo", "systemctl", "enable", "mysql"])

        # Настройка пароля root пользователя
        subprocess.run(["sudo", "mysqladmin", "-u", "root", "password", password])

        # Удаление анонимного пользователя и запрет удаленного доступа к базе данных для root
        subprocess.run(["sudo", "mysql", "-u", "root", f"-p{password}", "-e", "DELETE FROM mysql.user WHERE User='';"])
        subprocess.run(["sudo", "mysql", "-u", "root", f"-p{password}", "-e", "DELETE FROM mysql.user WHERE User='root' AND Host NOT IN ('localhost', '127.0.0.1', '::1');"])
        subprocess.run(["sudo", "mysql", "-u", "root", f"-p{password}", "-e", "DROP DATABASE IF EXISTS test;"])
        subprocess.run(["sudo", "mysql", "-u", "root", f"-p{password}", "-e", "DELETE FROM mysql.db WHERE Db='test' OR Db='test\\_%';"])

        # Применение изменений привилегий
        subprocess.run(["sudo", "mysql", "-u", "root", f"-p{password}", "-e", "FLUSH PRIVILEGES;"])

        print("MySQL успешно установлен и настроен. Пароль сохранен в файл 'mysql_password.txt'")
    except Exception as e:
        print("Ошибка при установке MySQL:", e)

if __name__ == "__main__":
    install_mysql()
