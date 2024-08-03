import os


def delete_image(path: str) -> None:
    """Удаляет ненужные картинки."""
    try:
        os.remove(path)
    except FileNotFoundError:
        pass
