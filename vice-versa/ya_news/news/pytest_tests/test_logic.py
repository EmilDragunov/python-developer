from pytest_django.asserts import assertRedirects, assertFormError
import pytest
from news.forms import WARNING, BAD_WORDS
from http import HTTPStatus
from news.models import Comment
from .conftest import FORM_DATA


@pytest.mark.django_db
def test_anonymous_user_cant_create_comment(client, url_detail, url_login):
    count = Comment.objects.count()
    response = client.post(url_detail, FORM_DATA)
    expected_url = f"{url_login}?next={url_detail}"
    assertRedirects(response, expected_url)
    assert Comment.objects.count() == count


@pytest.mark.django_db
def test_create_comment_authorized_user(
    author_client, author, news, url_detail
):
    count = Comment.objects.count()
    response = author_client.post(url_detail, FORM_DATA)
    assert response.status_code == HTTPStatus.FOUND
    assertRedirects(
        response,
        url_detail + '#comments'
    )
    assert Comment.objects.count() == count + 1
    new_comment = Comment.objects.get(text=FORM_DATA['text'])
    assert new_comment.text == FORM_DATA['text']
    assert new_comment.news == news
    assert new_comment.author == author


@pytest.mark.django_db
@pytest.mark.parametrize('bad_word', BAD_WORDS)
def test_user_cant_use_bad_words(author_client, url_detail, bad_word):
    count = Comment.objects.count()
    bad_words_data = {'text': f'Какой-то текст, {bad_word}, еще текст'}
    response = author_client.post(url_detail, data=bad_words_data)
    assert response.status_code == HTTPStatus.OK
    assertFormError(response, 'form', 'text', WARNING)
    assert Comment.objects.count() == count


@pytest.mark.django_db
def test_edit_comment_author_client(
    author_client, comment, url_edit, url_detail
):
    response = author_client.post(url_edit, FORM_DATA)
    assert response.status_code == HTTPStatus.FOUND
    assertRedirects(response, url_detail + '#comments')
    comment = Comment.objects.get(pk=comment.id)
    comment.refresh_from_db()
    assert comment.text == FORM_DATA['text']


@pytest.mark.django_db
def test_edit_comment_not_author_client(not_author_client, url_edit):
    response = not_author_client.post(url_edit, FORM_DATA)
    assert response.status_code == HTTPStatus.NOT_FOUND


@pytest.mark.django_db
def test_delete_comment_author_client(author_client, comment, url_delete):
    count = Comment.objects.count()
    response = author_client.post(url_delete)
    assert response.status_code == HTTPStatus.FOUND
    assert Comment.objects.count() == count - 1
    with pytest.raises(Comment.DoesNotExist):
        Comment.objects.get(pk=comment.id)


@pytest.mark.django_db
def test_delete_comment_not_author_client(
    not_author_client, comment, news, url_delete
):
    count = Comment.objects.count()
    response = not_author_client.post(url_delete)
    assert response.status_code == HTTPStatus.NOT_FOUND
    assert Comment.objects.count() == count
    comment.refresh_from_db()
    assert comment.text == comment.text
    assert comment.news == news
    assert comment.author == comment.author
