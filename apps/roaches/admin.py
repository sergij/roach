from django.contrib import admin
from roaches.models import BaseSkillType, Level, Status, Garment, Box, Roach, RaceRoad, Race, Point, Harm, RuningLog, Avatar, ResultDroped, EvolutionPrice

admin.site.register(BaseSkillType)
admin.site.register(Level)
admin.site.register(Status)
admin.site.register(Garment)
admin.site.register(Box)
admin.site.register(Race)
admin.site.register(RaceRoad)
admin.site.register(Roach)
admin.site.register(Point)
admin.site.register(Harm)
admin.site.register(RuningLog)
admin.site.register(Avatar)
admin.site.register(ResultDroped)
admin.site.register(EvolutionPrice)