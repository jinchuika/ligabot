from django.db import models


class Team(models.Model):
    id = models.PositiveIntegerField(primary_key=True)
    name = models.CharField(max_length=128)
    code = models.CharField(max_length=4, null=True)
    short_name = models.CharField(max_length=64, null=True)
    squad_market_value = models.CharField(max_length=32, null=True)
    crest_url = models.URLField(null=True, blank=True)

    class Meta:
        verbose_name = "Team"
        verbose_name_plural = "Teams"

    def __str__(self):
        return self.name


class Competition(models.Model):
    id = models.PositiveIntegerField(primary_key=True)
    caption = models.CharField(max_length=100)
    league = models.CharField(max_length=4, null=True)
    year = models.CharField(max_length=4)
    numberOfTeams = models.IntegerField(null=True)
    numberOfGames = models.IntegerField(null=True)
    numberOfMatchdays = models.IntegerField(null=True)
    currentMatchday = models.IntegerField(null=True)
    lastUpdated = models.DateTimeField(null=True)

    teams = models.ManyToManyField(Team, blank=True)

    class Meta:
        verbose_name = "Competition"
        verbose_name_plural = "Competitions"

    def __str__(self):
        return self.caption


class Fixture(models.Model):
    id = models.PositiveIntegerField(primary_key=True)
    competition = models.ForeignKey(Competition, related_name='fixtures')
    date = models.DateTimeField()
    status = models.CharField(max_length=15, null=True, blank=True)
    matchday = models.PositiveIntegerField(null=True)
    home_team = models.ForeignKey(Team, related_name='home_fixtures', null=True)
    away_team = models.ForeignKey(Team, related_name='away_fixtures', null=True)
    goals_home = models.IntegerField(default=0, null=True)
    goals_away = models.IntegerField(default=0, null=True)

    class Meta:
        verbose_name = "Fixture"
        verbose_name_plural = "Fixtures"

    def __str__(self):
        return '{} - {}'.format(self.home_team, self.away_team)
