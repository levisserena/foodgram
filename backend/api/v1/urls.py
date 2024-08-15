from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import (IngredientViewSer, RecipeViewSet, TagViewSet,
                    UserFoodgramViewSet, redirect_short_link)

router_recipes = DefaultRouter()
router_recipes.register('recipes', RecipeViewSet,
                        basename='recipes')
router_recipes.register('ingredients', IngredientViewSer,
                        basename='ingredients')
router_recipes.register('tags', TagViewSet,
                        basename='tags')
router_recipes.register('users', UserFoodgramViewSet,
                        basename='users')

urlpatterns = [
    path('api/auth/', include('djoser.urls.authtoken')),
    path('api/', include(router_recipes.urls)),
    path('s/<str:short>/', redirect_short_link, name='redirect_short_link')
]
