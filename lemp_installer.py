import os
import subprocess
from mysql_installer import install_mysql

def run_command(command):
    print(f"Executing: {command}")
    return os.system(command)

def install_lemp():
    #Установка дополнительных утилит
    run_command("sudo apt install net-tools mc htop zip unzip p7zip-full dialog certbot python3-certbot-nginx -y")
    
    # Установка Nginx
    run_command("sudo apt update")
    run_command("sudo apt install nginx -y")

    # Установка PHP
    run_command("sudo apt install php8.1 php8.1-{fpm,curl,pdo,cli,bcmath,bz2,curl,intl,gd,mbstring,mysql,zip,xml} -y")
  
    # Настройка PHP-FPM
    php_fpm_conf_file = '/etc/php/8.1/fpm/pool.d/www.conf'  # Путь к файлу конфигурации PHP-FPM (может отличаться в разных версиях Ubuntu)
    with open(php_fpm_conf_file, 'r') as f:
        php_conf = f.read()
    php_conf = php_conf.replace('www-data', 'www-data')
    with open(php_fpm_conf_file, 'w') as f:
        f.write(php_conf)
    # Вызов функции установки mysql
    install_mysql() #Здесь есть проблема
    
    # Перезапуск служб
    run_command("sudo systemctl restart nginx")
    run_command("sudo systemctl restart php8.1-fpm")
    run_command("sudo systemctl restart mysql")


    print("LEMP установлен и настроен успешно!")

if __name__ == "__main__":
    install_lemp()
