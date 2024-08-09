#!/bin/bash
echo "Create user..."
python manage.py shell -c "
from django.contrib.auth import get_user_model;
UserModel = get_user_model(); 
UserModel.objects.create_superuser(first_name='Лев', last_name='Акчурин', username='levis', email='levisserena@yandex.ru', password='a741852456');
UserModel.objects.create_user(first_name='Игорь', last_name='Фракин', username='igor', email='igor@yandex.ru', password='a741852456');
UserModel.objects.create_user(first_name='user0', last_name='user0', username='user0', email='user0@r.ru', password='DjangoUser0');
UserModel.objects.create_user(first_name='user1', last_name='user1', username='user1', email='user1@r.ru', password='DjangoUser1');
UserModel.objects.create_user(first_name='user2', last_name='user2', username='user2', email='user2@r.ru', password='DjangoUser2');
UserModel.objects.create_user(first_name='user3', last_name='user3', username='user3', email='user3@r.ru', password='DjangoUser3');
UserModel.objects.create_user(first_name='user4', last_name='user4', username='user4', email='user4@r.ru', password='DjangoUser4');
UserModel.objects.create_user(first_name='user5', last_name='user5', username='user5', email='user5@r.ru', password='DjangoUser5');
UserModel.objects.create_user(first_name='user6', last_name='user6', username='user6', email='user6@r.ru', password='DjangoUser6');
UserModel.objects.create_user(first_name='user7', last_name='user7', username='user7', email='user7@r.ru', password='DjangoUser7');
UserModel.objects.create_user(first_name='user8', last_name='user8', username='user8', email='user8@r.ru', password='DjangoUser8');
UserModel.objects.create_user(first_name='user9', last_name='user9', username='user9', email='user9@r.ru', password='DjangoUser9');
UserModel.objects.create_user(first_name='user10', last_name='user10', username='user10', email='user10@r.ru', password='DjangoUser10');
UserModel.objects.create_user(first_name='user11', last_name='user11', username='user11', email='user11@r.ru', password='DjangoUser11');
UserModel.objects.create_user(first_name='user12', last_name='user12', username='user12', email='user12@r.ru', password='DjangoUser12');
UserModel.objects.create_user(first_name='user13', last_name='user13', username='user13', email='user13@r.ru', password='DjangoUser13');
UserModel.objects.create_user(first_name='user14', last_name='user14', username='user14', email='user14@r.ru', password='DjangoUser14');
UserModel.objects.create_user(first_name='user15', last_name='user15', username='user15', email='user15@r.ru', password='DjangoUser15');
UserModel.objects.create_user(first_name='user16', last_name='user16', username='user16', email='user16@r.ru', password='DjangoUser16');
UserModel.objects.create_user(first_name='user17', last_name='user17', username='user17', email='user17@r.ru', password='DjangoUser17');
UserModel.objects.create_user(first_name='user18', last_name='user18', username='user18', email='user18@r.ru', password='DjangoUser18');
UserModel.objects.create_user(first_name='user19', last_name='user19', username='user19', email='user19@r.ru', password='DjangoUser19');
UserModel.objects.create_user(first_name='user20', last_name='user20', username='user20', email='user20@r.ru', password='DjangoUser20');
UserModel.objects.create_user(first_name='user21', last_name='user21', username='user21', email='user21@r.ru', password='DjangoUser21');
UserModel.objects.create_user(first_name='user22', last_name='user22', username='user22', email='user22@r.ru', password='DjangoUser22');
UserModel.objects.create_user(first_name='user23', last_name='user23', username='user23', email='user23@r.ru', password='DjangoUser23');
UserModel.objects.create_user(first_name='user24', last_name='user24', username='user24', email='user24@r.ru', password='DjangoUser24');
UserModel.objects.create_user(first_name='user25', last_name='user25', username='user25', email='user25@r.ru', password='DjangoUser25');
UserModel.objects.create_user(first_name='user26', last_name='user26', username='user26', email='user26@r.ru', password='DjangoUser26');
UserModel.objects.create_user(first_name='user27', last_name='user27', username='user27', email='user27@r.ru', password='DjangoUser27');
UserModel.objects.create_user(first_name='user28', last_name='user28', username='user28', email='user28@r.ru', password='DjangoUser28');
UserModel.objects.create_user(first_name='user29', last_name='user29', username='user29', email='user29@r.ru', password='DjangoUser29');
UserModel.objects.create_user(first_name='user30', last_name='user30', username='user30', email='user30@r.ru', password='DjangoUser30');
count = UserModel.objects.all().count()
print(f'Total entries made: {count}.')
"
echo "...user created."