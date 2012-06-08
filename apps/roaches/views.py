# -*- coding: utf-8 -*-
from django.core.context_processors import request
from django.http import HttpResponseRedirect
from django.shortcuts import render_to_response
#from django.contrib.auth.models import Group
from django.contrib.auth.decorators import login_required
#from django.contrib.auth.admin import User
from django.views.decorators.csrf import csrf_protect
from django.template import RequestContext
from django import forms

from roach.main.models import Base_skill_type, Level, Status, Artefact, Box, Roach, RaceRoad, Race, Point, Harm, RuningLog, Avatar

import datetime
import random


from main.models import Race

class DaysForm(forms.Form):
    #days = forms.Text(label=u"Период в днях")
    pass
    
@csrf_protect
def home_page(request):
    form = DaysForm()
    return render_to_response('index.html',{'user':request.user,'form':form, }, 
                               context_instance=RequestContext(request))

@csrf_protect
@login_required
def delete_races(request):
    """
    Производим удаление устарелых гонок,
    за указаный период request.POST['days']
    """
    if request.method == 'POST':
        if request.user.is_superuser:
            d = datetime.timedelta(days = int(request.POST['days']))
            try:
                race = Race.objects.order_by('date')[:1]
                date = race[0]
                new_date = date.date + d
                Race.objects.filter(date__lt=new_date).delete()
            except: pass
        return render_to_response('index.html',{'user':request.user, }, 
                               context_instance=RequestContext(request))
    return render_to_response('index.html',{'user':request.user, }, 
                               context_instance=RequestContext(request))

class WorkingForm(forms.Form):
    hours = forms.ChoiceField(label=u"Сколько часов собираешся проработать?",choices = ([('1','1 час'), ('2','2 часа'), ('3','3 часa'),('4','4 часa'),('5','5 часов'),('6','6 часов'),('7','7 часов'),('8','8 часов'),]), initial='1',)

class TrainingForm(forms.Form):
    hours = forms.ChoiceField(label=u"Сколько часов собираешся пропотеть?",choices = ([('1','1 час'), ('2','2 часа'), ('3','3 часa'),('4','4 часa'),('5','5 часов'),('6','6 часов'),('7','7 часов'),('8','8 часов'),]), initial='1',)

class RoachForm(forms.ModelForm):
    sex = forms.ChoiceField(label=u'Пол таракана',choices = ([('1','Mуж.'), ('0','Жен.'), ]), initial='1',)
    base_skill_type = forms.ModelChoiceField(label=u'Специализация таракана',queryset=Base_skill_type.objects.all(),initial='1') 
    class Meta:
        model = Roach
        fields = ('roach_name',)
    
class ChooseOpponent(forms.Form):
    level = forms.ModelChoiceField(label=u'Сила противника',queryset=Level.objects.all(), initial='0',)
        
def get_roach(out_id):
    try: roach = Roach.objects.get(out_id = out_id)
    except Roach.DoesNotExist:
        try: roach = Roach.objects.get(vk_id = out_id)
        except Roach.DoesNotExist: return None
    return roach

def regenerate_roach(roach):
    """
    Функция регенерации жизни таракана
    """
    if roach.power < roach.level.max_power:
        time = roach.regenerate_time
        delta = datetime.datetime.now() - time
        roach.regenerate_time = datetime.datetime.now()
        if delta.days>0:
            roach.power+=(float(roach.level.max_power)/60)*(delta.days*24*60)
        roach.power+=int((float(roach.level.max_power)/60)*delta.seconds/60)
        if roach.power > roach.level.max_power:
            roach.power = roach.level.max_power
            roach.save()
        roach.save()

def what_are_doing(roach):
    """
    Определяет чем же таки занят таракан в даный момент времени
    """
    time = roach.end_time_status
    d = time - datetime.datetime.now()
    hours = d.seconds/3600
    minutes = (d.seconds%3600)/60
    stat_time = [{'hours': hours, 'minutes': minutes, 'seconds': d.seconds-minutes*60-hours*3600,},]
    #stat_time.append({'hours': hours})
    #stat_time.append({})
    #stat_time.append({})
    if roach.status == Status.objects.get(status_name = "work"):
        stat_time.append({'mes': u"Вы сейчас на работе", 'val': "work"})
        #stat_time.append({})
        return stat_time
    elif roach.status == Status.objects.get(status_name = "train"):
        stat_time.append({'mes': u"Вы сейчас на репетиции балета", 'val': "train"})
        #stat_time.append({})
        return stat_time
    return stat_time
    
@csrf_protect
@login_required
def game_main(request):
    """
    Переводит юзера в Игру
    """
    roach = get_roach(out_id = request.user.id)
    if roach is None:
        return create_roach(request)
    #Проверка свободен ли сейчас таракан
    #if roach.status == Status.objects.get(status_name = "free"):
    regenerate_roach(roach)
    if roach.status == Status.objects.get(status_name = "work"):
        time = roach.end_time_status
        if time < datetime.datetime.now():
            roach.status = Status.objects.get(status_name = "free")
            roach.money_2 += roach.temp_money
            roach.temp_money = 0
            roach.save()
            return render_to_response('main/main.html',{'user':request.user, 'roach':roach}, 
                               context_instance=RequestContext(request))
        d = time - datetime.datetime.now()
        hours = d.seconds/3600
        minutes = (d.seconds%3600)/60
        seconds = d.seconds-minutes*60-hours*3600
        return render_to_response('main/main.html',{'user':request.user, 'roach':roach,'work':True, 'hours': hours, 'minutes':minutes, 'seconds':seconds}, 
                               context_instance=RequestContext(request))
    elif roach.status == Status.objects.get(status_name = "train"):
        time = roach.end_time_status
        if time < datetime.datetime.now():
            roach.status = Status.objects.get(status_name = "free")
            roach.exp_now += roach.temp_money
            roach.temp_money = 0
            roach.save()
            return render_to_response('main/main.html',{'user':request.user, 'roach':roach}, 
                               context_instance=RequestContext(request))
        d = time - datetime.datetime.now()
        hours = d.seconds/3600
        minutes = (d.seconds%3600)/60
        seconds = d.seconds-minutes*60-hours*3600
        return render_to_response('main/main.html',{'user':request.user, 'roach':roach,'train':True, 'hours': hours, 'minutes':minutes, 'seconds':seconds}, 
                               context_instance=RequestContext(request))
    return render_to_response('main/main.html',{'user':request.user, 'roach':roach}, 
                               context_instance=RequestContext(request))

@csrf_protect
@login_required
def create_roach(request):
    """
    Создание таракана юзеру
    """
    error = None
    form = RoachForm(request.POST or None)
    if form.is_valid():
        try: Roach.objects.get(roach_name = request.POST['roach_name'])
        except Roach.DoesNotExist:
            try: Roach.objects.get(out_id = request.user.id)
            except Roach.DoesNotExist:
                box = Box()
                box.save()
                roach = Roach(roach_name = form.cleaned_data['roach_name'])
                roach.out_id = request.user.id
                roach.sex = request.POST['sex']
                #if request.POST['base_skill_type']=="0":
                roach_skill = Base_skill_type.objects.get(id = request.POST['base_skill_type'])
                roach.avatar = Avatar.objects.get(male=request.POST['sex'], skill=roach_skill)
                roach.box = box
                roach.status = Status.objects.get(status_name="free")
                roach.level = Level.objects.get(level = 1)
                roach.save()
                return HttpResponseRedirect('/game/')
            error = u"""У вас уже есть один таракан!"""
            return render_to_response('main/create_roach.html',{'errors':error, 'user':request.user, 'form':form}, 
                               context_instance=RequestContext(request))
        error = u"Таракан с именем %s уже существует"%request.POST['roach_name']
    return render_to_response('main/create_roach.html',{'errors':error, 'user':request.user, 'form':form}, 
                               context_instance=RequestContext(request))
    
@csrf_protect
@login_required
def choose_opponent(request, roach_id):
    """
    Создание гонки
    """
    error = None
    if request.method == 'POST':
        roach = Roach.objects.get(id = request.POST['id'])
        while True:
            roaches = Roach.objects.all().exclude(id = request.POST['id'])
            opponent = roaches[random.randint(0,len(roaches)-1)]
            if opponent.power < (opponent.level.max_power/2): regenerate_roach(opponent)
            if opponent.power > (opponent.level.max_power/2): break
        return render_to_response('main/race_manager.html',{'error':error,'opponent':opponent, 'roach':roach}, 
                                  context_instance=RequestContext(request))
    else:
        roach = Roach.objects.get(id = roach_id)
        '''Блок проверок на возможность проведения поединка'''
        if roach.power < (roach.level.max_power/2):
            error = u"Ты ещё не отошел от предыдущей гонки."
            return render_to_response('main/main.html',{'error':error, 'user':request.user, 'roach':roach}, 
                                    context_instance=RequestContext(request))
        elif roach.status == Status.objects.get(status_name = "free"):
            while True:
                roaches = Roach.objects.all().exclude(id = roach.id)
                opponent = roaches[random.randint(0,len(roaches)-1)]
                if opponent.power < (opponent.level.max_power/2): regenerate_roach(opponent)
                if opponent.power > (opponent.level.max_power/2): break
            return render_to_response('main/race_manager.html',{'errors':error,'opponent':opponent, 'roach':roach},
                                       context_instance=RequestContext(request))
        else:
            temp = what_are_doing(roach)
            return render_to_response('main/main.html',{'error':temp[1]['mes'],'user':request.user, 'roach':roach,temp[1]['val']: True, 
                                                    'hours': temp[0]['hours'], 'minutes':temp[0]['minutes'], 'seconds':temp[0]['seconds']}, 
                                                    context_instance=RequestContext(request))

def clars(roach_1, roach_2):
    """
    Создание лога гонки по двум заданым тараканам
    Трасса(точки) - для менее сильного
    carma_<ID> - результат гонки для каждого таракана
    чем больше тем лучше
    pen_<ID> - пенальти за каждую точку (больше-лучше)
    """
    level = min(roach_1.level.level, roach_2.level.level)
    points = Point.objects.filter(race_road = RaceRoad.objects.get(level = level))
    carma_1 = 0
    carma_2 = 0
    log = []
    for i in xrange(len(points)):
        pen_1 = 0
        pen_2 = 0
        if random.random()<float(roach_1.trick_skill)/(roach_1.trick_skill+roach_2.trick_skill):
            harms = Harm.objects.all()
            harm = harms[random.randint(0,len(harms)-1)]
            if random.random()<float(roach_2.agil_skill)/(roach_1.agil_skill+roach_2.agil_skill):
                text = (harm.harm_text).replace('roach1',roach_1.roach_name)
                text = text.replace('roach2',roach_2.roach_name)
                log.append({0:text})
                text = (harm.unharm_text).replace('roach1',roach_1.roach_name)
                text = text.replace('roach2',roach_2.roach_name)
                log.append({0:text})
            else:
                text = (harm.harm_text).replace('roach1',roach_1.roach_name)
                text = text.replace('roach2',roach_2.roach_name)
                log.append({0:text})
        if random.random()<float(roach_2.trick_skill)/(roach_1.trick_skill+roach_2.trick_skill):
            harms = Harm.objects.all()
            harm = harms[random.randint(0,len(harms)-1)]
            if random.random()<float(roach_1.agil_skill)/(roach_1.agil_skill+roach_2.agil_skill):
                text = (harm.harm_text).replace('roach1',roach_2.roach_name)
                text = text.replace('roach2',roach_1.roach_name)
                log.append({0:text})
                text = (harm.unharm_text).replace('roach1',roach_2.roach_name)
                text = text.replace('roach2',roach_1.roach_name)
                log.append({0:text})
            else:
                text = (harm.harm_text).replace('roach1',roach_2.roach_name)
                text = text.replace('roach2',roach_1.roach_name)
                log.append({0:text})
        pen_1 = (not points[i].pow_skill==0)*roach_1.pow_skill - points[i].pow_skill + (not points[i].speed_skill==0)*roach_1.speed_skill - points[i].speed_skill + (not points[i].intel_skill==0)*roach_1.intel_skill - points[i].intel_skill   
        pen_2 = (not points[i].pow_skill==0)*roach_2.pow_skill - points[i].pow_skill + (not points[i].speed_skill==0)*roach_2.speed_skill - points[i].speed_skill + (not points[i].intel_skill==0)*roach_2.intel_skill - points[i].intel_skill
        roach_1.power-=points[i].power
        roach_2.power-=points[i].power
        try: text = points[i].runinglog_set.get(value = pen_1)
        except: text = points[0].runinglog_set.all()[0]
        log.append({0:text.text.replace('roach',roach_1.roach_name)})
        carma_1 += pen_1
        carma_2 += pen_2
    from roach.main.models import ResultDroped
    if carma_1 >= carma_2:
        winner = roach_1
        diff = roach_2.level.level - roach_1.level.level
        try: result = ResultDroped.objects.get(differenc = diff)
        except: pass
        if not result is None:
            roach_1.exp_now += result.exp
    else:
        winner = roach_2
        diff = roach_1.level.level - roach_2.level.level
        try: result = ResultDroped.objects.get(differenc = diff)
        except: pass
        if not result is None:
            roach_2.exp_now += result.exp
    ans = [{"winner":winner},]
    ans.append({'log':log})
    roach_1.regenerate_time = datetime.datetime.now()
    roach_2.regenerate_time = datetime.datetime.now()
    roach_1.save()
    roach_2.save()
    race = Race(road = RaceRoad.objects.get(level = level),
                               winner = winner.id,
                               prize = 0,
                               log = log)
    race.save()
    race.roaches.add(roach_1,roach_2)
    return race.id

@csrf_protect
@login_required
def create_race(request):
    """
    Создание гонки GET - запрос не расматриваеться,
    все выбирается в  /compete/
    """
    if request.method == 'POST':
        roach_1 = Roach.objects.get(id = request.POST['my_id'])
        roach_2 = Roach.objects.get(id = request.POST['id'])
        race_id = clars(roach_1, roach_2)
        #print log[0]["winner"]
        #return render_to_response('main/race_result.html',{'roach':roach_1, 'winner':log[0]["winner"], 'opponent':roach_2, 'log':log[1]['log']}, context_instance=RequestContext(request))
        return view_race(request, race_id, roach_1.id)
    return HttpResponseRedirect('/game/')

@csrf_protect
@login_required
def work_for_food(request, roach_id):
    """
    Устраиваем таракана на работу
    """
    roach = Roach.objects.get(id = roach_id)
    form = WorkingForm(request.POST or None)
    if roach.status == Status.objects.get(status_name = "free"):
        if form.is_valid():
            hours = int(form.cleaned_data['hours'])
            if hours > 0:
                roach.status = Status.objects.get(status_name = 'work')
                roach.end_time_status = datetime.datetime.now()+datetime.timedelta(hours=hours)
                roach.temp_money = roach.level.price_for_work*hours
                roach.save()
            return HttpResponseRedirect('/game/')
    else:
        temp = what_are_doing(roach)
        #print temp
        return render_to_response('main/main.html',{'error':temp[1]['mes'],'user':request.user, 'roach':roach,temp[1]['val']: True, 
                                                    'hours': temp[0]['hours'], 'minutes':temp[0]['minutes'], 'seconds':temp[0]['seconds']}, 
                                                    context_instance=RequestContext(request))
    return render_to_response('main/work.html',{'roach':roach,'form':form}, context_instance=RequestContext(request))

@csrf_protect
@login_required
def work_abort(request, roach_id):
    roach = Roach.objects.get(id = roach_id)
    roach.status = Status.objects.get(status_name = "free")
    roach.temp_money = 0
    roach.save()
    return render_to_response('main/main.html',{'user':request.user, 'roach':roach}, 
                                      context_instance=RequestContext(request))
    
@csrf_protect
@login_required
def train(request, roach_id):
    """
    Отдаем таракана тренеру
    """
    roach = Roach.objects.get(id = roach_id)
    form = TrainingForm(request.POST or None)
    if roach.status == Status.objects.get(status_name = "free"):
        if form.is_valid():
            hours = int(form.cleaned_data['hours'])
            if hours > 0:
                roach.status = Status.objects.get(status_name = "train")
                roach.end_time_status = datetime.datetime.now()+datetime.timedelta(hours = hours)
                roach.temp_money = roach.level.price_for_work*hours
                roach.money_2 -= hours*roach.level.price_for_work/2
                roach.save()
            return HttpResponseRedirect('/game/')
    else:
        temp = what_are_doing(roach)
        #print temp
        return render_to_response('main/main.html',{'error':temp[1]['mes'],'user':request.user, 'roach':roach,temp[1]['val']: True, 
                                                    'hours': temp[0]['hours'], 'minutes':temp[0]['minutes'], 'seconds':temp[0]['seconds']}, 
                                                    context_instance=RequestContext(request))
    return render_to_response('main/train.html',{'roach':roach,'form':form}, context_instance=RequestContext(request))

@csrf_protect
@login_required
def train_abort(request, roach_id):
    """
    Отменяем тренеровку таракана, при этом
    начисляем таракану опыта в соответствии
    с проведенным на тренеровке вемени
    """
    roach = Roach.objects.get(id = roach_id)
    roach.status = Status.objects.get(status_name = "free")
    time = roach.end_time_status
    d = time - datetime.datetime.now()
    hours = d.seconds/3600 + 1
    koef = roach.temp_money/roach.level.price_for_work
    roach.exp_now += (koef-hours)*roach.level.price_for_work
    roach.temp_money = 0
    roach.save()
    return render_to_response('main/main.html',{'user':request.user, 'roach':roach}, 
                                      context_instance=RequestContext(request))
@csrf_protect
@login_required 
def view_race(request, race_id, roach_id):
    #print log[0]["winner"]
    race = Race.objects.get(id = race_id)
    roach = Roach.objects.get(id = roach_id)
    winner = Roach.objects.get(id = race.winner)
    prize = race.prize
    roach_2 = race.roaches.all().exclude(id = roach.id)[0]
    exec(compile('log='+race.log, '<string>', 'exec'))
    return render_to_response('main/race_result.html',{'roach':roach, 'prize':prize, 'winner':winner, 'opponent':roach_2, 'log':log}, context_instance=RequestContext(request))

@csrf_protect
@login_required 
def view_stats(request, roach_id):
    #print log[0]["winner"]
    roach = Roach.objects.get(id = roach_id)
    roaches = Roach.objects.order_by('-exp_all')[:5]
    return render_to_response('main/stat.html',{'roach':roach, 'roaches':roaches,}, context_instance=RequestContext(request))

@csrf_protect
@login_required 
def evolution(request, roach_id):
    #print log[0]["winner"]
    roach = Roach.objects.get(id = roach_id)
    return render_to_response('main/evolution.html',{'roach':roach,}, context_instance=RequestContext(request))
