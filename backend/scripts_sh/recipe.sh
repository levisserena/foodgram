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
        image=f'recipes/images/test_r{i}.jpg'
    ) for i in range(1, NUMBER_RECIPE + 1)
])
recipe_id = Recipe.objects.values_list('id', flat=True)
ing_id_list = Ingredient.objects.values_list('id', flat=True)
tag_id_list = Tag.objects.values_list('id', flat=True)
def get_ing(): return sample([i for i in ing_id_list], randint(1, 4))
def get_tag(): return sample([i for i in tag_id_list], randint(1, 2))
def rec_ing():
    ing_id = get_ing()
    for i_id in ing_id:
        RecipeIngredient.objects.bulk_create([
            RecipeIngredient(
                recipe=Recipe.objects.get(id=r_id),
                ingredient=Ingredient.objects.get(id=i_id),
                amount=randrange(10, 2000, 10),
            ) for r_id in recipe_id
        ])
def rec_tag():
    tag_id = get_ing()
    for t_id in tag_id:
        RecipeTag.objects.bulk_create([
            RecipeTag(
                recipe=Recipe.objects.get(id=r_id),
                tag=Tag.objects.get(id=t_id),
            ) for r_id in recipe_id
        ])
rec_ing()
rec_tag()
count = Recipe.objects.all().count()
print(f'Total entries made: {count}.')
"
echo "...recipes created."