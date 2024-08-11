#!/bin/bash
echo "Create favorit..."
python manage.py shell -c "
from random import randint
from users.models import User
from recipes.models import Favoritism, Recipe
user_id = User.objects.values_list('id', flat=True)
recipe_id = Recipe.objects.values_list('id', flat=True)
Favoritism.objects.bulk_create([
    Favoritism(user=User.objects.get(id=f'{i}'), recipe=Recipe.objects.get(id=f'{k}')) for i in user_id for k in recipe_id if randint(1, 30) == 18
])
count = Favoritism.objects.all().count()
print(f'Total entries made: {count}.')
"
echo "...favorit created."