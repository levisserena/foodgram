#!/bin/bash
echo "Create token..."
python manage.py shell -c "
from rest_framework.authtoken.models import Token
from users.models import User
user_id = User.objects.values_list('id', flat=True)
for i in user_id:
    Token.objects.get_or_create(user=User.objects.get(id=f'{i}'))
count = Token.objects.all().count()
print(f'Total entries made: {count}.')
"
echo "...token created."