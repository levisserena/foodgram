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

Важно! Скрипты будут падать с ошибками, если база данных предварительно заполнена.


В последствии, для выпуска продукта пользователю, достаточно запустить
следующие скрипты

sudo docker compose exec backend sh scripts_sh/migrate.sh
sudo docker compose exec backend sh scripts_sh/ingredient.sh
sudo docker compose exec backend sh scripts_sh/tag.sh
sudo docker compose exec backend sh scripts_sh/static.sh

Или запустить один который запустит остальные:

sudo docker compose exec backend sh scripts_sh/prod.sh