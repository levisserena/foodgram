from django.contrib.admin import ModelAdmin, display, register, site
from django.contrib.auth.admin import UserAdmin
from django.utils.translation import gettext_lazy as _

from .models import Follow, User

site.site_title = 'Админ-зона Foodgram.'
site.site_header = 'Админ-зона Foodgram.'


@register(User)
class UserFoodgramAdmin(UserAdmin):
    """Для управления пользователями в админ зоне."""

    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        (_('Personal info'), {'fields': ('first_name', 'last_name', 'email',
                                         ('avatar', 'get_html_avatar'))}),
        (_('Permissions'), {
            'fields': ('is_active', 'is_staff', 'is_superuser'),
        }),
        (_('Important dates'), {'fields': ('last_login', 'date_joined')}),
    )

    list_display = ('id', 'get_full_name', 'email', 'is_active')
    list_display_links = ('id', 'get_full_name')
    list_editable = ('is_active',)
    search_fields = ('username', 'email', 'last_name', 'first_name')
    readonly_fields = ('id', 'date_joined', 'get_html_avatar')
    ordering = ('-is_superuser', '-is_staff', 'username')
    search_help_text = ('Можно искать по username, имени и фамилии, а '
                        'также e-mail.')

    @display(description='Миниатюра')
    def get_html_avatar(self, object):
        """Возвращает миниатюру."""
        return object.get_html_avatar

    @display(description='Имя пользователя')
    def get_full_name(self, object):
        """Возвращает полное имя."""
        return f'{object.last_name} {object.first_name} ({object.username})'


@register(Follow)
class FollowAdmin(ModelAdmin):
    """Модель для администрирования подписок."""

    fields = (
        ('user', 'get_html_avatar_user'),
        ('following', 'get_html_avatar_following'),
    )
    list_display = ('id', 'get_following')
    list_display_links = ('id', 'get_following')
    readonly_fields = (
        'get_html_avatar_user',
        'get_html_avatar_following',
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
                        'подписчика, так и на кого подписывались.')

    @display(description='')
    def get_html_avatar_user(self, object):
        """Возвращает миниатюру того, кто подписан."""
        return object.user.get_html_avatar

    @display(description='')
    def get_html_avatar_following(self, object):
        """Возвращает миниатюру того, кто подписан."""
        return object.following.get_html_avatar

    @display(description='Подписки')
    def get_following(self, object):
        """Возвращает кто на кого подписан."""
        return f'{object.user} подписан на {object.following}'
