from django.conf import settings
import pytest
from news.forms import CommentForm


@pytest.mark.django_db
def test_home_page_news_count(client, news_all, url_home):
    response = client.get(url_home)
    assert response.context_data[
        'object_list'
    ].count() <= settings.NEWS_COUNT_ON_HOME_PAGE
    assert 'object_list' in response.context_data


@pytest.mark.django_db
def test_home_page_news_order(client, news_all, url_home):
    response = client.get(url_home)
    object_list = response.context['object_list']
    all_dates = [news.date for news in object_list]
    sorted_dates = sorted(all_dates, reverse=True)
    assert all_dates == sorted_dates


@pytest.mark.django_db
def test_news_detail_page_comments_order(
    client, comment_all, url_detail
):
    response = client.get(url_detail)
    assert 'news' in response.context
    news = response.context['news']
    all_comments = news.comment_set.all()
    all_timestamps = [comment.created for comment in all_comments]
    sorted_timestamps = sorted(all_timestamps)
    assert all_timestamps == sorted_timestamps


@pytest.mark.django_db
def test_news_detail_page_comment_form_availability_for_anonymous_user(
    client, url_detail
):
    response = client.get(url_detail)
    assert 'form' not in response.context


@pytest.mark.django_db
def test_news_detail_page_comment_form_availability_for_author(
    author_client, url_detail
):
    response = author_client.get(url_detail)
    assert 'form' in response.context
    assert isinstance(response.context['form'], CommentForm)
