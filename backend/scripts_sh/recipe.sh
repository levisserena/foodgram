#!/bin/bash
echo "Create recipes..."
python manage.py shell -c "
from random import choice, choices, randint, randrange, sample
from users.models import User
from recipes.models import Ingredient, Recipe, Tag, RecipeIngredient, RecipeTag
NUMBER_USER = 30
NUMBER_RECIPE = 150
NAME_1 = ('Жаренная', 'Паренная', 'Варенная', 'Печеная', 'Копченая')
NAME_2 = ('морковь', 'капуста', 'картошка', 'морошка', 'пелемешка')
ACTION = ('варить ', 'жарить ', 'парить ', 'мешать ', 'дать потомится ')
def get_name(name): return ''.join(choice(name))
def get_action(): return ''.join(choices(ACTION, k=6))
Recipe.objects.bulk_create([
    Recipe(
        name=f'{get_name(NAME_1)} {get_name(NAME_2)}',
        text=f'Берём чистую кастрюлю...{get_action()}. Готово!',
        author=User.objects.get(id=randint(1, NUMBER_USER)),
        cooking_time=randint(1, 120),
        # image='recipes/images/test.jpg'
    ) for _ in range(1, NUMBER_RECIPE + 1)
])
recipe_id = Recipe.objects.values_list('id', flat=True)
ing_id_list = Ingredient.objects.values_list('id', flat=True)
tag_id_list = Tag.objects.values_list('id', flat=True)
ing_id = sample([i for i in ing_id_list], 3)
tag_id = sample([i for i in tag_id_list], 2)
def rec_ing(ing_id):
    RecipeIngredient.objects.bulk_create([
        RecipeIngredient(
            recipe=Recipe.objects.get(id=i),
            ingredient=Ingredient.objects.get(id=ing_id),
            amount=randrange(10, 2000, 10),
        ) for i in recipe_id
    ])
def rec_tag(tag_id):
    RecipeTag.objects.bulk_create([
        RecipeTag(
            recipe=Recipe.objects.get(id=i),
            tag=Tag.objects.get(id=tag_id),
        ) for i in recipe_id
    ])
rec_ing(ing_id[0])
if randint(1, 5) >= 3: rec_ing(ing_id[1])
if randint(1, 5) >= 1: rec_ing(ing_id[2])
rec_tag(tag_id[0])
if randint(1, 5) >= 1: rec_tag(tag_id[1])
count = Recipe.objects.all().count()
print(f'Total entries made: {count}.')
"
echo "...recipes created."