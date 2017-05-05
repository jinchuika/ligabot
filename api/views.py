from .serializers import MatchSerializer, TableSerializer
from rest_framework import generics
from api.api_request import RequestHandler


class TeamMatchListView(generics.ListAPIView):
    serializer_class = MatchSerializer

    def get_queryset(self):
        req = RequestHandler()
        return req.get_team_scores(self.kwargs['team_id'])


class LeagueMatchListView(generics.ListAPIView):
    serializer_class = MatchSerializer

    def get_queryset(self):
        req = RequestHandler()
        return req.get_league_scores(self.kwargs['league_id'])


class LeagueStandingListView(generics.ListAPIView):
    serializer_class = TableSerializer

    def get_queryset(self):
        req = RequestHandler()
        return req.get_standings(self.kwargs['league_id'])
