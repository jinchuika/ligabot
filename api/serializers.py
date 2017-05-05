from rest_framework import serializers


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
