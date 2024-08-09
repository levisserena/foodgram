from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import (  # avatar,
                    IngredientViewSer,
                    redirect_short_link,
                    RecipeViewSet,
                    TagViewSet,
                    UserFoodgramViewSet)


router_recipes = DefaultRouter()
router_recipes.register(
    'recipes',
    RecipeViewSet,
    basename='recipes',
)
router_recipes.register(
    'ingredients',
    IngredientViewSer,
    basename='ingredients',
)
router_recipes.register(
    'tags',
    TagViewSet,
    basename='tags'
)
router_recipes.register(
    'users',
    UserFoodgramViewSet,
    basename='users'
)

urlpatterns = [
    # path('users/me/avatar/', avatar, name='avatar'),
    path('auth/', include('djoser.urls.authtoken')),
    path('', include(router_recipes.urls)),
    # path('', include('djoser.urls.base')),
    path('s/<str:short>/', redirect_short_link, name='redirect_short_link')
]
