#!/bin/bash
echo "Create follow..."
python manage.py shell -c "
from random import randint
from users.models import Follow, User
user_id = User.objects.values_list('id', flat=True)
Follow.objects.bulk_create([
    Follow(user=User.objects.get(id=f'{i}'), following=User.objects.get(id=f'{k}')) for i in user_id for k in user_id if (i != k and randint(1, 87) <= 18)
])
count = Follow.objects.all().count()
print(f'Total entries made: {count}.')
"
echo "...follow created."