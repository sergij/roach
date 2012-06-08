# -*- coding: utf-8 -*-
from django.db import models

def upload_picture(instance, filename):
    """Generates upload path for ImageField"""
    return u"upload/avatar/%s" % filename.replace(' ','_')

def temp_upload(instance, filename):
    """Generates upload path for FileField"""
    return u"uploads/admin/%s" % (filename.replace(' ','_'))
 
class Base_skill_type(models.Model):
    skill_name = models.CharField(u"Базовый скил",max_length = 50)
    volume_prize = models.IntegerField(u"Бонус скила",default = 0)
    def __unicode__(self):
        return self.skill_name

class Avatar(models.Model):
    male = models.BooleanField(default = False)
    skill = models.ForeignKey(Base_skill_type, blank = True, null = True)
    image  = models.ImageField(upload_to=upload_picture)
    def __unicode__(self):
        if self.skill:
            return  str(self.male) + ' '+ self.skill.skill_name+ ' ' + ' ' + str(self.image.name).split('/')[-1]
        else:
            return str(self.male) + ' ' + str(self.image.name).split('/')[-1]
    class Meta:
        ordering = ["id"]
    
class Level(models.Model):
    level_name = models.CharField(u"Уровень",max_length = 50)
    level = models.IntegerField(default = 1)
    max_power = models.IntegerField(default = 100)
    price_for_work = models.IntegerField(default = 10)
    exp_to_next_lvl = models.IntegerField(default = 24)
    class Meta:
        ordering = ['level']
    def __unicode__(self):
        return self.level_name
    
class Status(models.Model):
    status_name = models.CharField(u"Статус игрока",max_length = 50)
    def __unicode__(self):
        return self.status_name
    
class Artefact(models.Model):
    artefact_name = models.CharField(u"Одежка",max_length = 50)
    img = models.ImageField(u"Вид одежки",upload_to=temp_upload)
    def __unicode__(self):
        return self.artefact_name

class Box(models.Model):
    artefacts = models.ManyToManyField(Artefact, null=True)
    def __unicode__(self):
        return u"Сундук " + str(self.id)

class Roach(models.Model):
    vk_id = models.IntegerField(blank = True, null = True)
    out_id = models.IntegerField(blank = True, null = True)
    roach_name = models.CharField(u"Имя таракана",max_length = 100)
    avatar = models.ForeignKey(Avatar, blank = True, null = True)
    money_1 = models.IntegerField(u"Внешний капитал",default = 0)
    money_2 = models.IntegerField(u"Внутрений баланс",default = 0)
    temp_money = models.IntegerField(u"Возможный прирост",default = 0)
    sex = models.BooleanField(u"Пол таракана",default = False)
    pow_skill = models.IntegerField(u"Выносливость",default = 1)
    speed_skill = models.IntegerField(u"Скорость",default = 1)
    intel_skill = models.IntegerField(u"Интелект",default = 1)
    trick_skill = models.IntegerField(u"Хитрость",default = 1)
    agil_skill = models.IntegerField(u"Уворотливость",default = 1)
    power = models.IntegerField(u"Сила таракана",default = 15)
    exp_all = models.IntegerField(u"Опыт общий",default = 0)
    exp_now = models.IntegerField(u"Опыт текущий",default = 0)
    level = models.ForeignKey(Level)
    box = models.OneToOneField(Box)
    slot_1 = models.IntegerField(blank = True, null = True)
    slot_2 = models.IntegerField(blank = True, null = True)
    slot_3 = models.IntegerField(blank = True, null = True)
    slot_4 = models.IntegerField(blank = True, null = True)
    slot_5 = models.IntegerField(blank = True, null = True)
    regenerate_time = models.DateTimeField(blank = True, null = True)
    status = models.ForeignKey(Status)
    end_time_status = models.DateTimeField(auto_now_add=True)
    PREMIUM = models.BooleanField(u"Премиальный план",default = False)
    end_time_premium = models.DateTimeField(auto_now_add=True)
    is_banned = models.BooleanField(default = False)
    def __unicode__(self):
        return self.roach_name
    
class RaceRoad(models.Model):
    road_name = models.CharField(u"Название трассы",max_length = 100)
    img = models.ImageField(u"Картинка трассы",upload_to=temp_upload)
    level = models.ForeignKey(Level)
    points = models.IntegerField(default = 10)
    def __unicode__(self):
        return (self.road_name + ' ' + self.level.level_name)
        
class Point(models.Model):
    race_road = models.ForeignKey(RaceRoad)
    position = models.IntegerField(default = 1)
    pow_skill = models.IntegerField(default = 0)
    speed_skill = models.IntegerField(default = 0)
    intel_skill = models.IntegerField(default = 0)
    power = models.IntegerField(default = 0)
    class Meta:
        ordering = ['position']
    def __unicode__(self):
        return (self.race_road.road_name + ' ' + str(self.position))
    
class Race(models.Model):
    road = models.ForeignKey(RaceRoad)
    roaches = models.ManyToManyField(Roach)
    winner = models.IntegerField(u"Победитель",default = 0)
    prize = models.IntegerField(u"Очки за победу",default = 0)
    log = models.TextField(u"Лог гонки",max_length = 50000)
    date = models.DateTimeField(auto_now_add=True,blank=True,null=True)
    def __unicode__(self):
        return Roach.objects.get(id = self.winner).__unicode__()
    
class Harm(models.Model):
    harm_text = models.TextField(u"Текст подляны",max_length = 20000)
    unharm_text = models.TextField(u"Текст уворота",max_length = 20000)
    def __unicode__(self):
        return u'Подляна #' + str(self.id)
    
class RuningLog(models.Model):
    point = models.ForeignKey(Point,default = None)
    text = models.TextField(u"Текст прохода точки",max_length = 20000)
    value = models.IntegerField(u"Необходимый запас",default=0)
    class Meta:
        ordering = ['value']
    def __unicode__(self):
        return self.text[:30]
    
class ResultDroped(models.Model):
    differenc = models.IntegerField(u"Разница уровней бегунов", default=0)
    perc_min = models.IntegerField(u"Миникальный сбиваемый процент", default=7)
    perc_max = models.IntegerField(u"Максимальный сбиваемый процент", default=10)
    exp = models.IntegerField(u"Опыт за победу", default=2)
    class Meta:
        ordering = ['differenc']
    def __unicode__(self):
        return str(self.differenc)+ ' ' + str(self.perc_min) + ' '+ str(self.perc_max)+ ' '+ str(self.exp)

class EvolutionPrice(models.Model):
    value = models.IntegerField(u"На что переходим", default=1)
    cost = models.IntegerField(u"Сколько стоит", default=1)
    class Meta:
        ordering = ['value']
    def __unicode__(self):
        return str(self.value)+ ' ' + str(self.cost)
