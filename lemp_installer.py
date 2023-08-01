import os

def run_command(command):
    print(f"Executing: {command}")
    return os.system(command)

def install_lemp():
    # Установка Nginx
    run_command("sudo apt update")
    run_command("sudo apt install nginx -y")
    
    # Установка MySQL
    run_command("sudo apt install mysql-server -y")
    run_command("sudo mysql_secure_installation")  # Настройка безопасности MySQL (можно пропустить)

    # Установка PHP
    run_command("sudo apt install php7.4-fpm php7.4-mysql php7.4-mbstring php7.4-xml php7.4-bcmath php7.4-gd php7.4-zip -y")
  
    # Настройка PHP-FPM
    php_fpm_conf_file = '/etc/php/7.4/fpm/pool.d/www.conf'  # Путь к файлу конфигурации PHP-FPM (может отличаться в разных версиях Ubuntu)
    with open(php_fpm_conf_file, 'r') as f:
        php_conf = f.read()
    php_conf = php_conf.replace('www-data', 'nginx')
    with open(php_fpm_conf_file, 'w') as f:
        f.write(php_conf)

    # Перезапуск служб
    run_command("sudo systemctl restart nginx")
    run_command("sudo systemctl restart php7.4-fpm")
    run_command("sudo systemctl restart mysql")
    
    print("LEMP установлен и настроен успешно!")

if __name__ == "__main__":
    install_lemp()
