import os
import subprocess
from mysql_installer import install_mysql

def run_command(command):
    print(f"Executing: {command}")
    return os.system(command)

def install_lemp():
    # Установка Nginx
    run_command("sudo apt update")
    run_command("sudo apt install nginx -y")

    # Установка PHP
    run_command("sudo apt install php8.1-fpm php8.1-mysql php8.1-mbstring php8.1-xml php8.1-bcmath php8.1-gd php8.1-zip -y")
  
    # Настройка PHP-FPM
    php_fpm_conf_file = '/etc/php/8.1/fpm/pool.d/www.conf'  # Путь к файлу конфигурации PHP-FPM (может отличаться в разных версиях Ubuntu)
    with open(php_fpm_conf_file, 'r') as f:
        php_conf = f.read()
    php_conf = php_conf.replace('www-data', 'nginx')
    with open(php_fpm_conf_file, 'w') as f:
        f.write(php_conf)
    # Вызов функции установки mysql
    install_mysql() //Здесь есть проблема
    
    # Перезапуск служб
    run_command("sudo systemctl restart nginx")
    run_command("sudo systemctl restart php7.4-fpm")
    run_command("sudo systemctl restart mysql")

    #Установка дополнительных утилит
    run_command("sudo apt install net-tools mc htop zip unzip p7zip-full -y")
    print("LEMP установлен и настроен успешно!")

if __name__ == "__main__":
    install_lemp()
