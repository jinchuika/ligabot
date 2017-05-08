from api.api_request import RequestHandler
from datetime import datetime
from api.models import Fixture, Competition, Team, TeamRank
from django.db.models import Q


class DBUpdater(object):
    def __init__(self, *args, **kwargs):
        self.req = RequestHandler(kwargs.get('verbose', False))

    def get_remote_leagues(self, league_id=None):
        if league_id:
            return self.req.get_league_info(league_id)
        else:
            this_year = datetime.now().year
            return self.req.get_leagues(this_year) + self.req.get_leagues(this_year - 1)

    def get_local_leagues(self):
        this_year = datetime.now().year
        return Competition.objects.filter(Q(year=this_year) | Q(year=(this_year - 1)))

    def get_remote_fixtures(self, league_id, time=1, show_upcoming=True):
        fixture_list = self.req.get_league_scores(league_id=league_id, time=time, show_upcoming=show_upcoming)
        return fixture_list

    def create_leagues(self):
        league_list = self.get_remote_leagues()
        created = []
        for league in league_list:
            try:
                comp = Competition.objects.get(id=league['id'])
            except Competition.DoesNotExist:
                comp = Competition(
                    id=league['id'],
                    caption=league['caption'],
                    league=league['league'],
                    year=league['year'],
                    numberOfTeams=league['numberOfTeams'],
                    numberOfGames=league['numberOfGames'],
                    numberOfMatchdays=league['numberOfMatchdays'],
                    currentMatchday=league['currentMatchday'],
                    lastUpdated=league['lastUpdated'])
                comp.save()
                created.append(comp)
        return created

    def create_teams(self, league_id):
        league = Competition.objects.get(id=league_id)
        team_list = self.req.get_league_teams(league_id)
        for team in team_list:
            try:
                new_team = Team.objects.get(id=team['id'])
            except Team.DoesNotExist:
                new_team = Team(
                    id=team['id'],
                    name=team['name'],
                    short_name=team['short_name'],
                    squad_market_value=team['squad_market_value'],
                    crest_url=team['crest_url'])
                new_team.save()
            TeamRank.objects.create(team=new_team, competition=league)
            league.save()
        return league

    def create_fixtures(self, league_id, time=6, show_upcoming=False):
        # Creates the fixtures for the last 6 days and for today
        league = Competition.objects.get(id=league_id)
        fixture_list = self.get_remote_fixtures(league_id, time=time, show_upcoming=show_upcoming) + self.get_remote_fixtures(league_id)
        for fixture in fixture_list:
            try:
                fix = Fixture.objects.get(id=fixture['id'])
            except Fixture.DoesNotExist:
                fix = Fixture(
                    id=fixture['id'],
                    competition=league,
                    date=datetime.strptime(fixture['fecha'], "%Y-%m-%dT%H:%M:%SZ"),
                    status=fixture['estado'],
                    matchday=fixture['jornada'],
                    home_team=Team.objects.get(id=fixture['local_id']),
                    away_team=Team.objects.get(id=fixture['visitante_id']),
                    goals_home=fixture['gol_local'],
                    goals_away=fixture['gol_visitante'],)
                fix.save()
        return league

    def update_league_scores(self, league_id):
        league = Competition.objects.get(id=league_id)
        remote_fixture_list = self.get_remote_fixtures(league_id)
        for remote_fixture in remote_fixture_list:
            try:
                local_fixture = Fixture.objects.get(Q(competition=league), ~Q(status='FINISHED'), Q(id=remote_fixture['id']))
                local_fixture.status = remote_fixture['estado']
                local_fixture.goals_home = remote_fixture['gol_local']
                local_fixture.goals_away = remote_fixture['gol_visitante']
                local_fixture.save()
                print("Updated: " + str(local_fixture))
            except Fixture.DoesNotExist:
                pass
        remote_league = self.get_remote_leagues(league_id)
        league.lastUpdated = datetime.strptime(remote_league['lastUpdated'], "%Y-%m-%dT%H:%M:%SZ")
        league.currentMatchday = remote_league['currentMatchday']
        league.save()
        return league

    def update_league_standings(self, league_id):
        remote_standings = self.req.get_standings(league_id)
        for standing in remote_standings:
            try:
                rank = TeamRank.objects.get(competition__id=league_id, team__id=standing['teamId'])
            except TeamRank.DoesNotExist:
                rank = TeamRank.objects.create(
                    competition__id=league_id,
                    team__id=standing['teamId'])
            rank.rank = standing['rank']
            rank.playedGames = standing["playedGames"]
            rank.goals = standing["goals"]
            rank.goalsAgainst = standing["goalsAgainst"]
            rank.goalDifference = standing["goalDifference"]
            rank.points = standing["points"]
            rank.save()
        return league_id
