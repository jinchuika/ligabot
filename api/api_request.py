import requests
import click
from django.conf import settings
from datetime import datetime


class RequestHandler(object):

    BASE_URL = settings.BASE_URL
    API_TOKEN = settings.API_TOKEN
    LIVE_URL = 'http://soccer-cli.appspot.com/'
    verbose = False

    def __init__(self, verbose=False):
        self.verbose = verbose

    def _get(self, url):
        """Handles api.football-data.org requests"""
        if self.verbose:
            print('calling: ' + url)
        req = requests.get(RequestHandler.BASE_URL + url, headers={'X-Auth-Token': RequestHandler.API_TOKEN, 'X-Response-Control': 'minified'})

        if req.status_code == requests.codes.ok:
            if self.verbose:
                print(req.text)
            return req

    def get_live_scores(self, use_12_hour_format):
        """Gets the live scores"""
        req = requests.get(RequestHandler.LIVE_URL)
        if req.status_code == requests.codes.ok:
            scores = req.json()
            if len(scores["games"]) == 0:
                click.secho("No live action currently", fg="red", bold=True)
                return
            self.writer.live_scores(scores, use_12_hour_format)
        else:
            click.secho("There was problem getting live scores", fg="red", bold=True)

    def get_team_scores(self, team_id, time=7, show_upcoming=False, use_12_hour_format=False):
        """Queries the API and gets the particular team scores"""
        time_frame = 'n' if show_upcoming else 'p'
        if team_id:
            req = self._get('teams/{team_id}/fixtures?timeFrame={time_frame}{time}'.format(
                team_id=team_id,
                time_frame=time_frame,
                time=time))
            team_scores = req.json()
            if len(team_scores["fixtures"]) != 0:
                return [{
                    'id': fixture['id'],
                    'fecha': fixture['date'],
                    'jornada': fixture['matchday'],
                    'local': fixture['homeTeamName'],
                    'visitante': fixture['awayTeamName'],
                    'gol_local': fixture['result']['goalsHomeTeam'],
                    'gol_visitante': fixture['result']['goalsAwayTeam'],
                    'estado': fixture["status"]
                } for fixture in team_scores['fixtures']]
        else:
            return []

    def get_standings(self, league_id):
        """Queries the API and gets the standings for a particular league"""
        req = self._get('competitions/{id}/leagueTable'.format(id=league_id))
        return [{
            'puesto': team["position"],
            'nombre': team["teamName"],
            'juegos': team["playedGames"],
            'goles_favor': team["goals"],
            'goles_contra': team["goalsAgainst"],
            'diferencia': team["goalDifference"],
            'puntos': team["points"]
        } for team in req.json()['standing']]

    def get_league_scores(self, league_id, time=7, show_upcoming=False, use_12_hour_format=False):

        """
        Queries the API and fetches the scores for fixtures
        based upon the league and time parameter
        """
        time_frame = 'n' if show_upcoming else 'p'
        if league_id:
            req = self._get('competitions/{league_id}/fixtures?timeFrame={time_frame}{time}'.format(
                league_id=league_id,
                time_frame=time_frame,
                time=time))
            fixtures_results = req.json()
            # no fixtures in the past week. display a help message and return
            if len(fixtures_results["fixtures"]) != 0:
                return [{
                    'id': fixture['id'],
                    'fecha': fixture['date'],
                    'jornada': fixture['matchday'],
                    'local': fixture['homeTeamName'],
                    'local_id': fixture['homeTeamId'],
                    'visitante_id': fixture['awayTeamId'],
                    'visitante': fixture['awayTeamName'],
                    'gol_local': fixture['result']['goalsHomeTeam'],
                    'gol_visitante': fixture['result']['goalsAwayTeam'],
                    'estado': fixture["status"]
                } for fixture in fixtures_results['fixtures']]
            else:
                return []
        else:
            # When no league specified. Print all available in time frame.
            return []

    def get_team_players(self, team):
        """
        Queries the API and fetches the players
        for a particular team
        """
        team_id = self.team_names.get(team, None)
        req = self._get('teams/{team_id}/players'.format(team_id=team_id))
        team_players = req.json()
        if int(team_players["count"]) == 0:
            click.secho("No players found for this team", fg="red", bold=True)
        else:
            self.writer.team_players(team_players)

    def get_leagues(self, season=None):
        if not season:
            season = datetime.now().year
        req = self._get('competitions/?season={season}'.format(season=season))
        competition_list = req.json()

        return [{
            'id': competition['id'],
            'caption': competition['caption'],
            'league': competition['league'],
            'year': competition['year'],
            'numberOfTeams': competition['numberOfTeams'],
            'numberOfGames': competition['numberOfGames'],
            'numberOfMatchdays': competition['numberOfMatchdays'],
            'currentMatchday': competition['currentMatchday'],
            'lastUpdated': competition['lastUpdated'],
        } for competition in competition_list]

    def get_league_info(self, league_id):
        req = self._get('competitions/{league_id}/'.format(league_id=league_id))
        competition = req.json()

        return {
            'id': competition['id'],
            'caption': competition['caption'],
            'league': competition['league'],
            'year': competition['year'],
            'numberOfTeams': competition['numberOfTeams'],
            'numberOfGames': competition['numberOfGames'],
            'numberOfMatchdays': competition['numberOfMatchdays'],
            'currentMatchday': competition['currentMatchday'],
            'lastUpdated': competition['lastUpdated'],
        }

    def get_league_teams(self, league_id):
        req = self._get('competitions/{league_id}/teams'.format(league_id=league_id))
        team_list = req.json()

        return [{
            'id': team['id'],
            'name': team['name'],
            'short_name': team['shortName'],
            'squad_market_value': team['squadMarketValue'],
            'crest_url': team['crestUrl'],
        } for team in team_list['teams'] if 'id' in team]
