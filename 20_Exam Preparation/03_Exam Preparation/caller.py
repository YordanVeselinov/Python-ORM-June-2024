import os
from decimal import Decimal

import django

# Set up Django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "orm_skeleton.settings")
django.setup()

# Import your models here
from main_app.models import Author, Review, Article
from django.db.models import Q, Count, Avg, Sum


# from populate_db import populate_model_with_data


# Create queries within functions


def get_authors(search_name=None, search_email=None) -> str:
    if search_name is None and search_email is None:
        return ''

    if search_name is not None and search_email is None:
        query = Q(full_name__icontains=search_name)
    elif search_email is not None and search_name is None:
        query = Q(email__icontains=search_email)
    else:
        query = Q(full_name__icontains=search_name) & Q(email__icontains=search_email)

    authors = Author.objects.filter(query).order_by('-full_name')

    result = []

    for a in authors:
        result.append(f'Author: {a.full_name}, email: {a.email}, status: {"Banned" if a.is_banned else "Not Banned"}')

    return '\n'.join(result)


def get_top_publisher() -> str:
    top_publisher = Author.objects.annotate(
        article_count=Count('articles')
    ).order_by(
        '-article_count',
        'email'
    ).first()

    if top_publisher is None or top_publisher.article_count == 0:
        return ''

    return f'Top Author: {top_publisher.full_name} with {top_publisher.article_count} published articles.'


def get_top_reviewer() -> str:
    top_reviewer = Author.objects.annotate(
        review_count=Count('reviews')
    ).order_by(
        '-review_count',
        'email'
    ).first()

    if top_reviewer is None or top_reviewer.review_count == 0:
        return ''

    return f'Top Reviewer: {top_reviewer.full_name} with {top_reviewer.review_count} published reviews.'


def get_latest_article() -> str:
    last_article = Article.objects.annotate(
        avg_reviews_rating=Avg('reviews__rating'),
        num_reviews=Count('reviews')
    ).order_by(
        '-published_on'
    ).first()

    if last_article is None or not last_article.authors:
        return ''

    authors = ', '.join(last_article.authors.order_by('full_name').values_list('full_name', flat=True))

    avg_reviews_rating = last_article.avg_reviews_rating if last_article.avg_reviews_rating is not None else 0.0

    return f'The latest article is: {last_article.title}. ' \
           f'Authors: {authors}. ' \
           f'Reviewed: {last_article.num_reviews} times. ' \
           f'Average Rating: {avg_reviews_rating:.2f}.'


def get_top_rated_article() -> str:
    top_rated_article = Article.objects.annotate(
        avg_rating=Avg('reviews__rating'),
        review_count=Count('reviews')
    ).filter(
        review_count__gt=0,
    ).order_by(
        '-avg_rating',
        'title',
    ).first()

    if not top_rated_article:
        return ''

    avg_rating_str = f"{top_rated_article.avg_rating:.2f}"

    return f'The top-rated article is: {top_rated_article.title}, ' \
           f'with an average rating of {avg_rating_str}, ' \
           f'reviewed {top_rated_article.review_count} times.'


def ban_author(email=None) -> str:
    if email is None:
        return 'No authors banned.'

    try:
        author = Author.objects.get(email=email)
    except Author.DoesNotExist:
        return "No authors banned."

    author.is_banned = True
    author.save()

    reviews = author.reviews.count()

    author.reviews.all().delete()

    return f'Author: {author.full_name} is banned! {reviews} reviews deleted.'
