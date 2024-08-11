#!/bin/bash
echo "Create user..."
python manage.py shell -c "
from random import choice
from users.models import User
User.objects.create_superuser(first_name='Лев', last_name='Акчурин', username='levis', email='levisserena@yandex.ru', password='a741852456')
User.objects.create_superuser(first_name='Игорь', last_name='Фракин', username='igor', email='igor@yandex.ru', password='a741852456')
NUMBER_USER = 30
NAME_1 = ('Соловьёва', 'Ласточкина', 'Коршунова', 'Воронина', 'Соколова', 'Кукушкина', 'Пингвинова')
NAME_2 = ('Алина', 'Светлана', 'Екатирина', 'Мария', 'Елизавета', 'Елена')
def get_name(name): return ''.join(choice(name))
for i in range(1, NUMBER_USER - 1):
    User.objects.create_user(first_name=get_name(NAME_2), last_name=get_name(NAME_1), username=f'user_{i}', email=f'user_{i}@ya.ru', password=f'DjangoUser{i}')
count = User.objects.all().count()
print(f'Total entries made: {count}.')
"
echo "...user created."