from django.contrib.auth import get_user_model
from django.contrib.auth.models import AbstractUser
from django.core.exceptions import ValidationError
from django.db.models import (CASCADE,
                              CharField,
                              EmailField,
                              ForeignKey,
                              ImageField,
                              IntegerField,
                              ManyToManyField,
                              Model,
                              TextField,
                              SET_NULL,
                              SlugField,
                              UniqueConstraint)

from backend.settings import INVALID_USER_NAMES


class UserFoodgram(AbstractUser):
    """Модель пользователей, для проекта Footgram."""

    REQUIRED_FIELDS = (
        'first_name',
        'last_name',
    )
    email = EmailField(
        verbose_name='Электронная почта',
        unique=True,
        blank=False,
        null=True,
        help_text=('Поле обязательное для заполнения. '
                   'Для каждого пользователя уникально.')
    )
    avatar = ImageField(
        verbose_name='Аватар',
        upload_to='users/',
        null=True,
        blank=True,
        default=None,
    )

    def __str__(self):
        """Строковое представление модели."""
        return (f'{self.last_name} {self.first_name}'
                if f'{self.last_name} {self.first_name}' != ' '
                else f'{self.username}')

    def clean(self):
        """Метод не позволит создать пользователя с именем "me"."""
        super().clean()
        if self.username in INVALID_USER_NAMES:
            raise ValidationError(
                'Недопустимое имя!'
            )


User = get_user_model()


class Follow(Model):
    """Модель для подписки на других пользователей."""

    user = ForeignKey(
        User,
        on_delete=CASCADE,
        related_name='fan',  # нужно?
        verbose_name='Кто подписывался',
    )
    following = ForeignKey(
        User,
        on_delete=CASCADE,
        related_name='following',
        verbose_name='На кого подписывался',
    )

    class Meta:
        """Метaданные."""

        verbose_name = 'Подписки'
        verbose_name_plural = 'Подписки'
        constraints = [
            UniqueConstraint(
                fields=['user', 'following'],
                name='unique_user_following'
            ),
        ]

    def __str__(self):
        """Метод отвечающий за строковое представление объекта."""
        return f'{self.user} подписан на {self.following}'

    def clean(self):
        """Метод не разрешает подписаться на самого себя."""
        if self.user == self.following:
            raise ValidationError(
                'Подписываться самому на себя нельзя!'
            )
