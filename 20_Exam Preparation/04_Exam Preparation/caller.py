import os
import django

from main_app.populate_db import populate_model_with_data

# Set up Django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "orm_skeleton.settings")
django.setup()

from django.db.models import Count

from main_app.models import Tournament, TennisPlayer, Match


# Import your models here

# Create queries within functions
def get_tournaments_by_surface_type(surface=None) -> str:
    if surface is None:
        return ''

    tournaments = Tournament.objects.annotate(
        matches_count=Count('matches')
    ).filter(
        surface_type__icontains=surface,
    ).order_by(
        '-start_date'
    )

    if not tournaments:
        return ''

    result = []

    [result.append(f'Tournament: {t.name}, start date: {t.start_date}, matches: {t.matches_count}') for t in
     tournaments]

    return '\n'.join(result)


def get_latest_match_info() -> str:
    match = Match.objects.prefetch_related(
        'players'
    ).order_by(
        '-date_played',
        '-pk'
    ).first()

    if not match:
        return ''

    players = match.players.order_by('full_name')
    player1_full_name = players.first().full_name
    player2_full_name = players.last().full_name
    winner_full_name = "TBA" if match.winner is None else match.winner.full_name

    return f'Latest match played on: {match.date_played}, ' \
           f'tournament: {match.tournament.name}, ' \
           f'score: {match.score}, ' \
           f'players: {player1_full_name} vs {player2_full_name}, ' \
           f'winner: {winner_full_name}, ' \
           f'summary: {match.summary}'


def get_matches_by_tournament(tournament_name=None) -> str:
    if tournament_name is None:
        return 'No matches found.'

    matches = Match.objects.select_related(
        'tournament',
        'winner'
    ).filter(
        tournament__name__exact=tournament_name,
    ).order_by('-date_played')

    if not matches:
        return 'No matches found.'

    result = []

    for m in matches:
        result.append(
            f'Match played on: {m.date_played}, score: {m.score}, winner: {"TBA" if not m.winner else m.winner.full_name}')

    return '\n'.join(result)


def get_tennis_players(search_name=None, search_country=None):
    if search_name is None and search_country is None:
        return ""

    if search_name is not None and search_country is not None:
        players = TennisPlayer.objects.filter(full_name__icontains=search_name, country__icontains=search_country)
    elif search_name is not None:
        players = TennisPlayer.objects.filter(full_name__icontains=search_name)
    else:
        players = TennisPlayer.objects.filter(country__icontains=search_country)

    if not players:
        return ""

    players = players.order_by('ranking')

    result = []

    [result.append(f"Tennis Player: {player.full_name}, country: {player.country}, ranking: {player.ranking}")
     for player in players]

    return '\n'.join(result)


def get_top_tennis_player():
    player = TennisPlayer.objects.get_tennis_players_by_wins_count().first()

    if player is None:
        return ''

    return f"Top Tennis Player: {player.full_name} with {player.wins} wins."


def get_tennis_player_by_matches_count():
    player_with_most_matches = TennisPlayer.objects.annotate(
        num_matches=Count('matches')
    ).order_by(
        '-num_matches',
        'ranking'
    ).first()

    if player_with_most_matches is not None and player_with_most_matches.num_matches:
        return f"Tennis Player: {player_with_most_matches.full_name} with " \
               f"{player_with_most_matches.num_matches} matches played."

    return ""

