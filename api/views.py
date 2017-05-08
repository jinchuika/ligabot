from django.db.models import Q
from .serializers import MatchSerializer, TableSerializer, CompetitionSerializer, FixtureSerializer, TeamSerializer
from rest_framework import mixins, generics, viewsets
from api.api_request import RequestHandler
from api.models import Competition, Fixture, Team


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


class FixtureViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = FixtureSerializer
    queryset = Fixture.objects.all()

    def get_queryset(self):
        queryset = Fixture.objects.all()
        competition_id = self.request.query_params.get('competition', None)
        team_id = self.request.query_params.get('team', None)
        home_id = self.request.query_params.get('home', None)
        away_id = self.request.query_params.get('away', None)
        if competition_id is not None:
            queryset = queryset.filter(competition__id=competition_id)
        if team_id is not None:
            queryset = queryset.filter(Q(home_team__id=team_id) | Q(away_team__id=team_id))
        if home_id is not None:
            queryset = queryset.filter(home_team__id=home_id)
        if away_id is not None:
            queryset = queryset.filter(away_team__id=away_id)
        return queryset


class CompetitionViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = CompetitionSerializer
    queryset = Competition.objects.all()


class TeamViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = TeamSerializer
    queryset = Team.objects.all()
