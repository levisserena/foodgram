#!/bin/bash
echo "Create favorit..."
python manage.py shell -c "
from random import randint
from users.models import User
from recipes.models import Recipe, ShopingCart
user_id = User.objects.values_list('id', flat=True)
recipe_id = Recipe.objects.values_list('id', flat=True)
ShopingCart.objects.bulk_create([
    ShopingCart(user=User.objects.get(id=f'{i}'), recipe=Recipe.objects.get(id=f'{k}')) for i in user_id for k in recipe_id if randint(1, 20) == 18
])
count = ShopingCart.objects.all().count()
print(f'Total entries made: {count}.')
"
echo "...favorit created."