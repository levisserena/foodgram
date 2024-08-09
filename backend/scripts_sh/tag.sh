#!/bin/bash
echo "Create tags..."
python manage.py shell -c "
from recipes.models import Tag;
Tag.objects.bulk_create([
Tag(name='Десерт', slug='dessert'),
Tag(name='Завтрак', slug='breakfast'),
Tag(name='Обед', slug='lunch'),
Tag(name='Ужин', slug='dinner'),
Tag(name='Аперитив', slug='aperitif'),
Tag(name='Ночной дожор', slug='nightwatch'),
])
count = Tag.objects.all().count()
print(f'Total entries made: {count}.')
"
echo "...tags created."