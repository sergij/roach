# -*- coding: utf-8 -*-
import os
from StringIO import StringIO
from datetime import datetime
import Image
import itertools

from django.conf import settings
from django.db import models, transaction
from django.contrib.auth.models import User

from django.utils.translation import ugettext_lazy as _
from django.core.validators import MinValueValidator, RegexValidator
from django.core.exceptions import ObjectDoesNotExist

from lib.fields import AutoOneToOneField
from lib.absmodels import TimestampedMixin, IndexedTimestampedMixin, TitledMixin, IndexedTimestampedSkipModifiedMixin
from lib.manager import manager_from

from manager_mixins import PublishedMixin, DeletedMixin, RoachMixin

def get_uuid_name_generator(prefix=''):
    import uuid
    def generator(instance, filename):
        ext = os.path.splitext(filename)[1]
        name = uuid.uuid4().hex + ext
        path = u'/'.join(filter(None, (prefix, name[:2], name[2:4], name)))
        return path
    return generator

class BaseSkillType(TitledMixin):
    volume_prize = models.IntegerField(u"Бонус скила",default = 0)
    
class Avatar(models.Model):
    male = models.BooleanField(default = False)
    skill = models.ForeignKey(BaseSkillType, blank = True, null = True)
    image  = models.ImageField(upload_to=get_uuid_name_generator('avatars'))

    class Meta:
        verbose_name = _(u'Аватар')
        verbose_name_plural = _(u'Аватары')
    
class Level(TitledMixin):
    level = models.IntegerField(default = 1, primary_key=True)
    max_power = models.IntegerField(default = 100)
    price_for_work = models.IntegerField(default = 10)
    exp_to_next_lvl = models.IntegerField(default = 24)
    class Meta:
        ordering = ['level']
    

class Garment(TitledMixin):
    img = models.ImageField(verbose_name=_(u"Вид одежки"),upload_to=get_uuid_name_generator('garment'))

    class Meta:
        verbose_name = _(u'Одежда')
        verbose_name_plural = _(u'Одежда')


class Box(models.Model):
    garment = models.ManyToManyField(Garment, null=True, blank=True)
    def __unicode__(self):
        return u"Сундук " + str(self.id)

    class Meta:
        verbose_name = _(u'Сундук с одеждой')
        verbose_name_plural = _(u'Сундуки')


class Roach(models.Model):
    STATUS_CHOICE = ( (0, _(u'свободен')), (1, _(u'работает')), (2, _(u'тренеруется')))
    GENDER_CHOICES = ( ('F', _(u'Женский')), ('M', _(u'Мужской')),)

    user = AutoOneToOneField(User, related_name='roach', primary_key=True)
    box = AutoOneToOneField(Box, verbose_name=u'Сундук', related_name='+')
    level = models.ForeignKey(Level)
    avatar = models.ForeignKey(Avatar, blank = True, null = True)
    nick = models.CharField(max_length=255, blank=True, default='', unique=True)

    money_1 = models.IntegerField(_(u"Внешний капитал"), default = 0)
    money_2 = models.IntegerField(_(u"Внутрений баланс"), default = 0)
    temp_money = models.IntegerField(_(u"Возможный прирост"), default = 0)
        
    gender = models.CharField(_(u'пол'), max_length=1, choices=GENDER_CHOICES,
                              null=True, blank=True)

    pow_skill = models.IntegerField(_(u"Выносливость"), default = 1)
    speed_skill = models.IntegerField(_(u"Скорость"), default = 1)
    intel_skill = models.IntegerField(_(u"Интелект"), default = 1)
    trick_skill = models.IntegerField(_(u"Хитрость"), default = 1)
    agil_skill = models.IntegerField(_(u"Уворотливость"), default = 1)
    power = models.IntegerField(_(u"Сила таракана"), default = 100)

    exp_all = models.IntegerField(_(u"Опыт общий"),default = 0)
    exp_now = models.IntegerField(_(u"Опыт текущий"),default = 0)

    slot_1 = models.IntegerField(blank = True, null = True)
    slot_2 = models.IntegerField(blank = True, null = True)
    slot_3 = models.IntegerField(blank = True, null = True)
    slot_4 = models.IntegerField(blank = True, null = True)
    slot_5 = models.IntegerField(blank = True, null = True)

    regenerate_time = models.DateTimeField(blank = True, null = True)
    end_time_status = models.DateTimeField(auto_now_add=True)

    is_banned = models.BooleanField(default = False)
    status = models.IntegerField(_(u'Состояние таракана'), choices=STATUS_CHOICE, db_index=True, default=0)

    objects = manager_from(RoachMixin)
    @staticmethod
    def for_user(user):
        try:
            return Roach.objects.get(user=user.id)
        except Roach.DoesNotExist:
            try:
                level = Level.objects.get(level=1)
            except Level.DoesNotExist:
                level = Level.objects.create(level=1, title=u'Начинающий')
            try:
                avatar = Avatar.objects.get(id=1)
            except Avatar.DoesNotExist:
                avatar = None
            new_box = Box.objects.create()
            return Roach.objects.create(nick=user.username, user=user, box=new_box, level=level, avatar=avatar)

    def __unicode__(self):
        return u'{0}, владелец: {1}'.format(self.nick if self.nick else self.user, self.user.username)

    def regenerate_roach(self):
        if self.power < self.level.max_power:
            time = self.regenerate_time
            delta = datetime.now() - time
            self.regenerate_time = datetime.now()
            if delta.days > 0:
                self.power += (float(self.level.max_power)/60)*(delta.days*24*60)
            self.power += int((float(self.level.max_power)/60)*delta.seconds/60)
            if self.power > self.level.max_power:
                self.power = self.level.max_power
                self.save()
            self.save()

    class Meta:
        verbose_name = _(u'Таракан')
        verbose_name_plural = _(u'Тараканы')
    
class RaceRoad(models.Model):
    road_name = models.CharField(_(u"Название трассы"), max_length = 100)
    img = models.ImageField(_(u"Картинка трассы"), upload_to=get_uuid_name_generator('road'))
    level = models.ForeignKey(Level)
    points = models.ManyToManyField('Point', related_name='raceroads')
    def __unicode__(self):
        return (self.road_name + ' ' + self.level.level_name)
    class Meta:
        ordering = ['level']
        verbose_name = _(u'Гоночная трасса')
        verbose_name_plural = _(u'Гоночные трассы')

class Point(models.Model):
    position = models.IntegerField(default = 1)
    pow_skill = models.IntegerField(default = 0)
    speed_skill = models.IntegerField(default = 0)
    intel_skill = models.IntegerField(default = 0)
    power = models.IntegerField(default = 0)
    class Meta:
        ordering = ['position']
        verbose_name = _(u'Контрольная точка')
        verbose_name_plural = _(u'Контрольные точки')

    def __unicode__(self):
        return (self.race_road.road_name + ' ' + str(self.position))
    
class Race(IndexedTimestampedSkipModifiedMixin):
    road = models.ForeignKey(RaceRoad)
    roaches = models.ManyToManyField(Roach)
    winner = models.ForeignKey(Roach, related_name='races', verbose_name=u"Победитель")
    prize = models.IntegerField(u"Очки за победу",default = 0)
    log = models.TextField(_(u'Лог гонки'), blank=True)
    
    def __unicode__(self):
        return u'Победитель: {0}, трасса: {1}, призовые: {2}'.format(winner, road, prize)
    
class Harm(models.Model):
    harm_text = models.TextField(u"Текст подляны",max_length = 20000)
    unharm_text = models.TextField(u"Текст уворота",max_length = 20000)
    def __unicode__(self):
        return u'Подляна #' + str(self.id)
    class Meta:
        verbose_name = _(u'Брутальное поведение')
        verbose_name_plural = _(u'Брутальные поведения')

class RuningLog(models.Model):
    point = models.ForeignKey(Point, related_name='logs', default = None)
    text = models.TextField(_(u"Текст прохода точки"))
    value = models.IntegerField(_(u"Необходимый запас"), default=0)

    class Meta:
        ordering = ['value']
    
    def __unicode__(self):
        return u'{0}'.format(self.text[:30])
    
class ResultDroped(models.Model):
    differenc = models.IntegerField(_(u"Разница уровней бегунов"), default=0)
    perc_min = models.IntegerField(_(u"Миникальный сбиваемый процент"), default=7)
    perc_max = models.IntegerField(_(u"Максимальный сбиваемый процент"), default=10)
    exp = models.IntegerField(_(u"Опыт за победу"), default=2)
    class Meta:
        ordering = ['differenc']
    def __unicode__(self):
        return u'{0}, {1}, {2}, {3}'.format(str(self.differenc), str(self.perc_min), str(self.perc_max), str(self.exp))

class EvolutionPrice(models.Model):
    level = models.ForeignKey(Level, verbose_name=u'Уровень перехода')
    cost = models.IntegerField(_(u"Сколько стоит"), default=1)
    
    class Meta:
        verbose_name = _(u'Стоимость перехода')
        verbose_name_plural = _(u'Стоимости переходов')

    def __unicode__(self):
        return u'{0}, стоимость {1}'.format(str(self.value), str(self.cost))
