from random import choice

from backend.settings import LENGTH_SHORT_LINK, STRING_CHARACTERS


def get_short_link(
        string_characters: str = STRING_CHARACTERS,
        range_pass: int = LENGTH_SHORT_LINK,
) -> str:
    """Генератор коротких ссылок.

    Принимает два аргумента: 
    * целое число - длина ссылки
    * строку - набор используемых символов.

    Возвращает сгенерированную ссылку в виде строки.
    """
    pass_list = [choice(string_characters) for _ in range(range_pass)]
    return ''.join(pass_list)
