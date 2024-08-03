from django.test import TestCase, Client
from notes.models import Note
from django.urls import reverse
from django.contrib.auth import get_user_model

User = get_user_model()


class BaseTestCase(TestCase):

    # Константы
    USERNAME_AUTHOR = 'Лев Толстой'
    USERNAME_ANOTHER_USER = 'Николай Гоголь'
    SLUG_NOTE = 'qwe'
    NOTE_TEXT = [
        'Заголовок',
        'Текст комментария',
        'qwe'
    ]
    NEW_NOTE_TEXT = [
        'Обновлённый комментарий',
        'Текст комментария Обновлённый',
        'qweasd'
    ]
    TITLE = 'Обновлённый комментарий'
    FORM_DATA_1 = {
        'title': 'Новый заголовок',
        'text': 'Новый текст',
        'slug': SLUG_NOTE
    }
    FORM_DATA_2 = {
        'title': 'Новый заголовок',
        'text': 'Новый текст',
    }
    CONTEXT_OBJECT_NAME = 'object_list'

    # Постоянные URL-ы
    HOME = 'notes:home'
    LOGIN = 'users:login'
    LOGOUT = 'users:logout'
    SIGNUP = 'users:signup'
    ADD = 'notes:add'
    SUCCESS = 'notes:success'
    LIST = 'notes:list'

    # Зависящие от константных текстовых данных URL-ы
    DETAIL = 'notes:detail'
    EDIT = 'notes:edit'
    DELETE = 'notes:delete'

    @classmethod
    def setUpTestData(cls):
        # Создаем юзеров и заметки
        cls.author = User.objects.create(username=cls.USERNAME_AUTHOR)
        cls.another_user = User.objects.create(
            username=cls.USERNAME_ANOTHER_USER
        )
        cls.note = Note.objects.create(
            title=cls.NOTE_TEXT[0], text=cls.NOTE_TEXT[1],
            slug=cls.SLUG_NOTE, author=cls.author
        )

        # Создаем авторизованных клиентов
        cls.auth_client = Client()
        cls.auth_client.force_login(cls.author)

        cls.another_client = Client()
        cls.another_client.force_login(cls.another_user)

        # Создаем URL-ы
        cls.detail_url = reverse(cls.DETAIL, args=(cls.note.slug,))
        cls.edit_url = reverse(cls.EDIT, args=(cls.note.slug,))
        cls.delete_url = reverse(cls.DELETE, args=(cls.note.slug,))
        cls.home_url = reverse(cls.HOME)
        cls.login_url = reverse(cls.LOGIN)
        cls.logout_url = reverse(cls.LOGOUT)
        cls.signup_url = reverse(cls.SIGNUP)
        cls.add_url = reverse(cls.ADD)
        cls.success_url = reverse(cls.SUCCESS)
        cls.list_url = reverse(cls.LIST)

        cls.form_data = {
            'title': cls.NEW_NOTE_TEXT[0],
            'text': cls.NEW_NOTE_TEXT[1],
            'slug': cls.NEW_NOTE_TEXT[2]
        }
