from .base import BaseTestCase
from http import HTTPStatus


class TestRoutes(BaseTestCase):

    def test_pages_availability(self):
        test_cases = [
            [self.home_url, self.client, HTTPStatus.OK],
            [self.login_url, self.client, HTTPStatus.OK],
            [self.logout_url, self.client, HTTPStatus.OK],
            [self.signup_url, self.client, HTTPStatus.OK],
            [self.add_url, self.auth_client, HTTPStatus.OK],
            [self.list_url, self.auth_client, HTTPStatus.OK],
            [self.success_url, self.auth_client, HTTPStatus.OK],
            [self.edit_url, self.auth_client, HTTPStatus.OK],
            [self.delete_url, self.auth_client, HTTPStatus.OK],
            [self.detail_url, self.auth_client, HTTPStatus.OK],
            [self.edit_url, self.another_client, HTTPStatus.NOT_FOUND],
            [self.delete_url, self.another_client, HTTPStatus.NOT_FOUND],
            [self.detail_url, self.another_client, HTTPStatus.NOT_FOUND],
        ]
        for url, client, expected_status_code in test_cases:
            with self.subTest(name=url):
                response = client.get(url)
                self.assertEqual(response.status_code, expected_status_code)

    def test_redirect_anonymous(self):
        for name in (
            self.add_url, self.list_url, self.success_url,
            self.edit_url, self.delete_url, self.detail_url
        ):
            with self.subTest(name=name):
                redirect_url = f'{self.login_url}?next={name}'
                response = self.client.get(name)
                self.assertRedirects(response, redirect_url)
