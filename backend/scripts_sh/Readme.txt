Ряд файлов со скриптами, для заполнения таблиц тестовыми данными.
Запустить скрипт надо находясь в папке с файлом manage.py.
Пример команды запуска:

sh scripts_sh/ingredient.sh

Чтобы запустить все скрипты, запустите скрипт start:

sh scripts_sh/start.sh

Те же команды, но для Docker compose:

docker compose exec backend sh scripts_sh/ingredient.sh
docker compose exec backend sh scripts_sh/start.sh

Возможно необходимо будет использовать sudo:

sudo docker compose exec backend sh scripts_sh/start.sh