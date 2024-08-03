from .base import BaseTestCase
from notes.forms import NoteForm


class TestDetailPage(BaseTestCase):

    def test_authorized_client_has_form(self):
        for url in [self.add_url, self.edit_url]:
            with self.subTest(url=url):
                response = self.auth_client.get(url)
                self.assertIn('form', response.context)
                self.assertIsInstance(response.context['form'], NoteForm)

    def test_author_sees_note(self):
        response = self.auth_client.get(self.list_url)
        self.assertIn(self.CONTEXT_OBJECT_NAME, response.context)
        self.assertIn(self.note, response.context[self.CONTEXT_OBJECT_NAME])

    def test_another_user_does_not_see_note(self):
        response = self.another_client.get(self.list_url)
        self.assertNotIn(self.note, response.context[self.CONTEXT_OBJECT_NAME])
