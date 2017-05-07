from .serializers import MatchSerializer, TableSerializer, CompetitionSerializer
from rest_framework import mixins
from rest_framework import generics
from api.api_request import RequestHandler
from api.models import Competition


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


class CompetitionApiView(mixins.ListModelMixin, generics.GenericAPIView):
    serializer_class = CompetitionSerializer
    queryset = Competition.objects.all()

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)
