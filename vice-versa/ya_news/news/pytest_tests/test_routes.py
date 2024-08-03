from http import HTTPStatus
import pytest
from pytest_django.asserts import assertRedirects


@pytest.mark.django_db
@pytest.mark.parametrize(
    'url, client_, code',
    (
        (
            pytest.lazy_fixture('url_home'),
            pytest.lazy_fixture('client'),
            HTTPStatus.OK
        ),
        (
            pytest.lazy_fixture('url_login'),
            pytest.lazy_fixture('client'),
            HTTPStatus.OK
        ),
        (
            pytest.lazy_fixture('url_logout'),
            pytest.lazy_fixture('client'),
            HTTPStatus.OK
        ),
        (
            pytest.lazy_fixture('url_signup'),
            pytest.lazy_fixture('client'),
            HTTPStatus.OK
        ),
        (
            pytest.lazy_fixture('url_detail'),
            pytest.lazy_fixture('client'),
            HTTPStatus.OK
        ),
        (
            pytest.lazy_fixture('url_edit'),
            pytest.lazy_fixture('author_client'),
            HTTPStatus.OK
        ),
        (
            pytest.lazy_fixture('url_delete'),
            pytest.lazy_fixture('author_client'),
            HTTPStatus.OK
        ),
        (
            pytest.lazy_fixture('url_edit'),
            pytest.lazy_fixture('not_author_client'),
            HTTPStatus.NOT_FOUND
        ),
        (
            pytest.lazy_fixture('url_delete'),
            pytest.lazy_fixture('not_author_client'),
            HTTPStatus.NOT_FOUND
        ),
    )
)
def test_status_codes(url, client_, code):
    assert client_.get(url).status_code == code


@pytest.mark.django_db
@pytest.mark.parametrize(
    'url, expected_url',
    (
        (pytest.lazy_fixture('url_edit'),
         pytest.lazy_fixture('url_login')),
        (pytest.lazy_fixture('url_delete'),
         pytest.lazy_fixture('url_login')),
    ),
)
def test_anonymous_redirects(url, expected_url, client):
    response = client.get(url)
    expected_url = f'{expected_url}?next={url}'
    assertRedirects(response, expected_url)
