from django.conf.urls import url
from django.contrib import admin
from rest_framework.urlpatterns import format_suffix_patterns
from api.views import TeamMatchListView, LeagueMatchListView, LeagueStandingListView

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^api/team/(?P<team_id>[+\d]+)/matches/$', TeamMatchListView.as_view(), name='team_match_list'),
    url(r'^api/league/(?P<league_id>[+\d]+)/$', LeagueMatchListView.as_view(), name='league_match_list'),
    url(r'^api/league/(?P<league_id>[+\d]+)/table/$', LeagueStandingListView.as_view(), name='league_match_list'),
]

urlpatterns = format_suffix_patterns(urlpatterns)
