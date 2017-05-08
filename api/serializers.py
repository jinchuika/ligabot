from rest_framework import serializers
from api.models import Competition, Fixture, Team


class MatchSerializer(serializers.Serializer):
    fecha = serializers.DateTimeField()
    local = serializers.CharField()
    visitante = serializers.CharField()
    gol_local = serializers.IntegerField()
    gol_visitante = serializers.IntegerField()
    estado = serializers.CharField()
    jornada = serializers.IntegerField()


class TableSerializer(serializers.Serializer):
    puesto = serializers.IntegerField()
    nombre = serializers.CharField()
    juegos = serializers.IntegerField()
    goles_favor = serializers.IntegerField()
    goles_contra = serializers.IntegerField()
    diferencia = serializers.IntegerField()
    puntos = serializers.IntegerField()


class CompetitionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Competition
        fields = '__all__'


class FixtureSerializer(serializers.ModelSerializer):
    home_team = serializers.StringRelatedField()
    away_team = serializers.StringRelatedField()

    class Meta:
        model = Fixture
        fields = '__all__'


class TeamSerializer(serializers.ModelSerializer):
    class Meta:
        model = Team
        fields = '__all__'
