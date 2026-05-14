Итоговая структура папок на сервере:

/var/www/filehost/

    ├── backend/

    ├── frontend/

    └── logs/


Инструкция по развёртыванию и запуску:

1. Установка системных пакетов.
Подключиться к серверу через консоль и выполнить команды:

    apt update && apt upgrade -y

    apt install -y \
    python3 \
    python3-pip \
    python3-venv \
    postgresql \
    postgresql-contrib \
    nginx \
    git

2. Создание директорий
    mkdir -p /var/www
    cd /var/www

3. Клонирование проекта
    git clone https://github.com/Kris-Polyakova/Diploma.git filehost

4. Backend виртуальное окружение
    cd /var/www/filehost/backend
    python3 -m venv venv
    source venv/bin/activate

5. Установка зависимостей
    pip install -r requirements.txt

6. Создание .env 
    nano .env

    SECRET_KEY=<надёжный пароль>

    DB_NAME=<имя базы данных>
    DB_USER=<логин для админа>
    DB_PASSWORD=<пароль для админа>
    DB_HOST=localhost
    DB_PORT=5432

7. PostgreSQL
    CREATE DATABASE <имя базы данных>;
    CREATE USER <логин для админа> WITH PASSWORD '<пароль для админа>';
    GRANT ALL PRIVILEGES ON DATABASE <имя базы данных> TO <логин для админа>;
    \c <имя базы данных>
    GRANT ALL ON SCHEMA public TO <логин для админа>;
    ALTER SCHEMA public OWNER TO <логин для админа>;
    \q

8. Django migrations
    cd /var/www/filehost/backend
    source venv/bin/activate
    python manage.py migrate

9. Superuser
    python manage.py createsuperuser

10. Gunicorn
    pip install gunicorn
    cd /var/www/filehost/backend/config
    nano settings.py
    добавить в ALLOWED_HOSTS IP-адрес сервера 
    и заодно добавить его в CORS_ALLOWED_ORIGINS и CSRF_TRUSTED_ORIGINS
    CORS_ALLOWED_ORIGINS = [
        "http://<SERVER_IP>",
        "127.0.0.1",
        "localhost",
    ]

    CSRF_TRUSTED_ORIGINS = [
        "http://<SERVER_IP>",
    ]

    и прописать STATIC_ROOT
    STATIC_URL = '/static/'
    STATIC_ROOT = BASE_DIR / 'static'

    cd /var/www/filehost/backend
    python manage.py collectstatic

    gunicorn config.wsgi:application --bind 0.0.0.0:8000
    http://<SERVER_IP>:8000/admin/ (проверка, должно работать)
    CTRL + C
    

11. Systemd service
    nano /etc/systemd/system/gunicorn.service

    содержимое файла:
        [Unit]
        Description=Gunicorn server for filehost
        After=network.target

        [Service]
        User=root
        Group=www-data

        WorkingDirectory=/var/www/filehost/backend

        EnvironmentFile=/var/www/filehost/backend/.env

        ExecStart=/var/www/filehost/backend/venv/bin/gunicorn \
        config.wsgi:application \
        --bind 127.0.0.1:8000 \
        --workers 2 \
        --timeout 120

        Restart=always

        [Install]
        WantedBy=multi-user.target

12. Запуск Gunicorn
    systemctl daemon-reload
    systemctl enable gunicorn
    systemctl restart gunicorn
    systemctl status gunicorn

13. Frontend
    curl -fsSL https://deb.nodesource.com/setup_20.x | sudo -E bash -
    sudo apt install -y nodejs
    npm install -g yarn
    yarn install
    yarn add @reduxjs/toolkit
    yarn add axios
    yarn build

14. Права nginx
    chown -R www-data:www-data /var/www/filehost
    chmod -R 755 /var/www/filehost

15. Nginx config
    nano /etc/nginx/sites-available/filehost

    содержимое файла:
        server {
            listen 80;

            server_name <SERVER_IP>;

            root /var/www/filehost/frontend/dist;
            index index.html;

            client_max_body_size 100M;

            location /assets/ {
                try_files $uri =404;

                access_log off;

                expires 1y;

                add_header Cache-Control "public, immutable";
            }

            location /static/ {
                alias /var/www/filehost/backend/static/;
            }

            location /media/ {
                alias /var/www/filehost/backend/media/;
            }

            location /api/ {
                proxy_pass http://127.0.0.1:8000;

                proxy_set_header Host $host;
                proxy_set_header X-Real-IP $remote_addr;
            }

            location /admin/ {
                proxy_pass http://127.0.0.1:8000;

                proxy_set_header Host $host;
                proxy_set_header X-Real-IP $remote_addr;
            }

            location / {
                try_files $uri /index.html;
            }
        }
    
16. Активация nginx
    ln -s /etc/nginx/sites-available/filehost /etc/nginx/sites-enabled/

17. Корректировка nginx конфигурации
    nano /etc/nginx/nginx.conf

    внутри http { }
    gzip off;

    sendfile off;
    tcp_nopush off;
    tcp_nodelay on;

    nginx -t (проверка)
    systemctl restart nginx

18. Права админа для admin
    Зайти в http://<SERVER_IP>/admin/ 
    В users дать администратору все права
