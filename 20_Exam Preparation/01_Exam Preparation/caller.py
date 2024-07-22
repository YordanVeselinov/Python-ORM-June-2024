import os
import django
from django.db.models import Count, Avg, Q, F

# Set up Django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "orm_skeleton.settings")
django.setup()

# Import your models here
from main_app.models import Director, Actor, Movie


# Create queries within functions
def get_directors(search_name=None, search_nationality=None) -> str:
    if search_name is None and search_nationality is None:
        return ''

    query_name = Q(full_name__icontains=search_name)
    query_nationality = Q(nationality__icontains=search_nationality)

    if search_name is None:
        query = query_nationality
    elif search_nationality is None:
        query = query_name
    else:
        query = Q(query_name & query_nationality)

    directors = Director.objects.filter(query).order_by('full_name')

    if not directors:
        return ''

    result = []

    for d in directors:
        result.append(f'Director: {d.full_name}, '
                      f'nationality: {d.nationality}, '
                      f'experience: {d.years_of_experience}')

    return '\n'.join(result)


def get_top_director() -> str:
    top_director = Director.objects.get_directors_by_movies_count().first()

    if not top_director:
        return ''

    return f'Top Director: {top_director.full_name}, movies: {top_director.movie_count}.'


def get_top_actor() -> str:
    top_actor = Actor.objects.prefetch_related('starring_actor_movies').annotate(
        movie_count=Count('starring_actor_movies'),
        average_rating=Avg('starring_actor_movies__rating'),
    ).order_by(
        '-movie_count',
        'full_name'
    ).first()

    if not top_actor or not top_actor.movie_count:
        return ''

    movies = ', '.join(m.title for m in top_actor.starring_actor_movies.all() if m)

    return f"Top Actor: {top_actor.full_name}, " \
           f"starring in movies: {movies}," \
           f" movies average rating: {top_actor.average_rating:.1f}"


def get_actors_by_movies_count() -> str:
    top_three_actors = Actor.objects.annotate(movies_count=Count('actor_movies')).order_by(
        '-movies_count', 'full_name'
    )[:3]

    if not top_three_actors or not top_three_actors[0].movies_count:
        return ''

    result = []

    for a in top_three_actors:
        result.append(f"{a.full_name}, participated in {a.movies_count} movies")

    return '\n'.join(result)


def get_top_rated_awarded_movie() -> str:
    top_movie = Movie.objects\
        .select_related('starring_actor')\
        .prefetch_related('actors')\
        .filter(is_awarded=True)\
        .order_by('-rating', 'title')\
        .first()

    if top_movie is None:
        return ''

    starring_actor = top_movie.starring_actor.full_name if top_movie.starring_actor else 'N/A'

    participating_actors = top_movie.actors.order_by('full_name').values_list('full_name', flat=True)

    cast = ', '.join(participating_actors)

    return f"Top rated awarded movie: {top_movie.title}, rating: {top_movie.rating:.1f}."\
            f" Starring actor: {starring_actor}. Cast: {cast}."


def increase_rating() -> str:
    movies_to_update = Movie.objects.filter(
        rating__lt=10,
        is_classic=True,
    )

    if not movies_to_update:
        return 'No ratings increased.'

    movie_count = movies_to_update.count()
    movies_to_update.update(rating=F('rating') + 0.1)

    return f'Rating increased for {movie_count} movies.'
