import csv
import os
from django.conf import settings
from django.core.management.base import BaseCommand
from reviews.models import (
    Category, Comment, Genre, Title, Review, GenreTitle
)
from reviews.models import User
DATA_DIRECTORY = os.path.join(settings.BASE_DIR, 'static/data/')


def users_to_db(row):
    User.objects.create(
        id=row[0],
        username=row[1],
        email=row[2],
        role=row[3],
        bio=row[4],
        first_name=row[5],
        last_name=row[6],
    )


def categories_to_db(row):
    Category.objects.create(
        id=row[0],
        name=row[1],
        slug=row[2],
    )


def genre_to_db(row):
    Genre.objects.create(
        id=row[0],
        name=row[1],
        slug=row[2],
    )


def titles_to_db(row):
    Title.objects.create(
        id=row[0],
        name=row[1],
        year=row[2],
        category_id=row[3],
    )


def genretitle_to_db(row):
    genre = Genre.objects.get(id=row[2])
    title = Title.objects.get(id=row[1])
    GenreTitle.objects.create(
        id=row[0],
        title=title,
        genre=genre,
    )


def review_to_db(row):
    title = Title.objects.get(id=row[1])
    Review.objects.create(
        id=row[0],
        title=title,
        text=row[2],
        author_id=row[3],
        score=row[4],
        pub_date=row[5],
    )


def comments_to_db(row):
    review = Review.objects.get(id=row[1])
    Comment.objects.create(
        id=row[0],
        review=review,
        text=row[2],
        author_id=row[3],
        pub_date=row[4],
    )


FILENAME_AND_ACTIONS = {
    'users.csv': users_to_db,
    'category.csv': categories_to_db,
    'genre.csv': genre_to_db,
    'titles.csv': titles_to_db,
    'genre_title.csv': genretitle_to_db,
    'review.csv': review_to_db,
    'comments.csv': comments_to_db,
}


class Command(BaseCommand):
    def handle(self, *args, **options):
        files = os.listdir(DATA_DIRECTORY)
        necessary_files = FILENAME_AND_ACTIONS.keys()
        if not set(files).issubset(necessary_files):
            files_not_found = list(set(necessary_files) - set(files))
            raise FileExistsError(
                f'Выполнение невозможно, отсутствуют файлы: {files_not_found}'
            )
        for file_name, action in FILENAME_AND_ACTIONS.items():
            file_path = DATA_DIRECTORY + file_name
            with open(file_path, encoding='utf-8') as f:
                file_reader = csv.reader(f, delimiter=',')
                next(file_reader)
                for row in file_reader:
                    action(row)
        print('Данные успешно загружены!')
