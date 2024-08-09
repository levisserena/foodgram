from django.contrib.admin import display, ModelAdmin, register, site
from django.utils.safestring import mark_safe

from .models import Follow, User

site.site_title = 'Админ-зона Foodgram.'
site.site_header = 'Админ-зона Foodgram.'


@register(User)
class UserFoodgramAdmin(ModelAdmin):
    """Для управления пользователями в админ зоне."""

    fields = (
        'id',
        'username',
        'email',
        ('last_name', 'first_name'),
        ('is_active', 'is_staff'),
        'date_joined',
        ('avatar', 'get_html_avatar'),
    )
    list_display = (
        'id',
        'username',
        'email',
        'get_full_name',
        'is_active',
    )
    list_display_links = (
        'id',
        'username',
    )
    list_editable = (
        'is_active',
    )
    search_fields = (
        'username',
        'email',
        'last_name',
        'first_name',
    )
    readonly_fields = (
        'id',
        'date_joined',
        'get_html_avatar',
    )
    ordering = (
        '-is_staff',
        'username',
    )

    @display(description='Миниатюра')
    def get_html_avatar(self, object):
        """Возвращает миниатюру."""
        if object.avatar:
            return mark_safe(f'<img src="{object.avatar.url}" width=70>')
        return 'Нет аватара'

    @display(description='Имя пользователя')
    def get_full_name(self, object):
        """Возвращает полное имя."""
        return f'{object.last_name} {object.first_name}'


@register(Follow)
class FollowAdmin(ModelAdmin):
    """Модель для администрирования подписок."""

    fields = (
        ('user', 'get_user_name'),
        ('following', 'get_following_name'),
    )
    list_display = (
        'id',
        'get_following',
    )
    list_display_links = (
        'id',
        'get_following',
    )
    readonly_fields = (
        'get_user_name',
        'get_following_name',
    )
    search_fields = (
        'user__username',
        'following__username',
        'user__last_name',
        'following__last_name',
        'user__first_name',
        'following__first_name',
    )
    search_help_text = ('Можно искать по username, имени и фамилии как'
                        'подписчика, так и на кого подписывались')

    @display(description='Имя того, кто подписан')
    def get_user_name(self, object):
        """Возвращает имя того, кто подписан."""
        return object.user.__str__()

    @display(description='Имя того, на кого подписан')
    def get_following_name(self, object):
        """Возвращает имя того, на кого подписан."""
        return object.following.__str__()

    @display(description='Подписки')
    def get_following(self, object):
        """Возвращает кто на кого подписан."""
        user = self.get_user_name(object)
        following = self.get_following_name(object)
        return f'{user} подписан на {following}'
