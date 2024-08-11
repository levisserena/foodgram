#!/bin/bash
echo "Create ingredient..."
python manage.py shell -c "
import json
from recipes.models import Ingredient
with open('scripts_sh/ingredients.json', 'r', encoding='utf-8') as read_file:
    data_json = json.load(read_file)
    Ingredient.objects.bulk_create([Ingredient(name=data['name'], measurement_unit=data['measurement_unit']) for data in data_json])
count = Ingredient.objects.all().count()
print(f'Total entries made: {count}.')
"
echo "...ingredient created."