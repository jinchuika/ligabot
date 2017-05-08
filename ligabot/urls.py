from django.conf.urls import url, include
from django.contrib import admin
from rest_framework.routers import DefaultRouter
from rest_framework.urlpatterns import format_suffix_patterns
from api.views import (TeamMatchListView, LeagueMatchListView,
	LeagueStandingListView, CompetitionApiView,
	FixtureViewSet, CompetitionViewSet, TeamViewSet)

router = DefaultRouter()
router.register(r'fixture', FixtureViewSet)
router.register(r'competition', CompetitionViewSet)
router.register(r'team', TeamViewSet)

urlpatterns = [
	url(r'^', include(router.urls)),
    url(r'^admin/', admin.site.urls),
    url(r'^api/team/(?P<team_id>[+\d]+)/matches/$', TeamMatchListView.as_view(), name='team_match_list'),
    url(r'^api/league/(?P<league_id>[+\d]+)/$', LeagueMatchListView.as_view(), name='league_match_list'),
    url(r'^api/league/(?P<league_id>[+\d]+)/table/$', LeagueStandingListView.as_view(), name='league_match_list'),
    url(r'^api/league/(?P<league_id>[+\d]+)/fixtures/$', FixtureViewSet.as_view({'get': 'list'}), name='league_fixture_list'),
    url(r'^api/league/$', CompetitionApiView.as_view(), name='league_list'),
]

# urlpatterns = format_suffix_patterns(urlpatterns)
