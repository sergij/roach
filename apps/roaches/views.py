# -*- coding: utf-8 -*-
from django.core.context_processors import request
from django.http import HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from django.shortcuts import  render, redirect, get_object_or_404
from roaches.models import BaseSkillType, Level, Status, Box, Roach, RaceRoad, Race, Point, Harm, Avatar

import datetime
import random
from roaches.forms import DaysForm

def index(request):
    form = DaysForm()
    return render(request, 'index.html', {'form': form})

@login_required
def delete_races(request):
    if request.method == 'POST':
        if request.user.is_superuser:
            d = datetime.timedelta(days = int(request.POST['days']))
            try:
                race = Race.objects.order_by('date')[:1]
                date = race[0]
                new_date = date.date + d
                Race.objects.filter(date__lt=new_date).delete()
            except: pass
        return render(request, 'index.html', {})
    return render(request, 'index.html', {})

def get_roach(out_id):
    try: roach = Roach.objects.get(out_id = out_id)
    except Roach.DoesNotExist:
        try: roach = Roach.objects.get(vk_id = out_id)
        except Roach.DoesNotExist: return None
    return roach



def what_are_doing(roach):
    time = roach.end_time_status
    d = time - datetime.datetime.now()
    hours = d.seconds/3600
    minutes = (d.seconds%3600)/60
    stat_time = [{'hours': hours, 'minutes': minutes, 'seconds': d.seconds-minutes*60-hours*3600,},]
    #stat_time.append({'hours': hours})
    #stat_time.append({})
    #stat_time.append({})
    if roach.status == Status.objects.get(pk=1):
        stat_time.append({'mes': u"Вы сейчас на работе", 'val': "work"})
        #stat_time.append({})
        return stat_time
    elif roach.status == Status.objects.get(pk=2):
        stat_time.append({'mes': u"Вы сейчас на репетиции балета", 'val': "train"})
        #stat_time.append({})
        return stat_time
    return stat_time
    
@login_required
def game(request):
    roach = Roach.for_user(request.user)
    roach.regenerate_roach()
    if roach.status.status == 1:
        time = roach.end_time_status
        if time < datetime.datetime.now():
            roach.status = Status.objects.get(pk=0)
            roach.money_2 += roach.temp_money
            roach.temp_money = 0
            roach.save()
            return render(request, 'roaches/main.html', {'roach': roach})
        d = time - datetime.datetime.now()
        hours = d.seconds/3600
        minutes = (d.seconds%3600)/60
        seconds = d.seconds-minutes*60-hours*3600
        return render(request, 'roaches/main.html',
            {'roach':roach,'work':True, 'hours': hours, 'minutes':minutes, 'seconds':seconds})
    elif roach.status.status == 1:
        time = roach.end_time_status
        if time < datetime.datetime.now():
            roach.status = Status.objects.get(pk=0)
            roach.exp_now += roach.temp_money
            roach.temp_money = 0
            roach.save()
            return render(request, 'roaches/main.html', {'roach': roach})
        d = time - datetime.datetime.now()
        hours = d.seconds/3600
        minutes = (d.seconds%3600)/60
        seconds = d.seconds-minutes*60-hours*3600
        return render(request, 'roaches/main.html', {'roach': roach, 'train': True, 'hours': hours, 'minutes':minutes, 'seconds':seconds})
    return render(request, 'roaches/main.html',{'roach':roach})

@login_required
def create_roach(request):
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
                roach_skill = BaseSkillType.objects.get(id = request.POST['base_skill_type'])
                roach.avatar = Avatar.objects.get(male=request.POST['sex'], skill=roach_skill)
                roach.box = box
                roach.status = Status.objects.get(status_name="free")
                roach.level = Level.objects.get(level = 1)
                roach.save()
                return HttpResponseRedirect('/game/')
            error = u"""У вас уже есть один таракан!"""
            return render(request, 'roaches/create_roach.html',{'errors':error, 'form':form})
        error = u"Таракан с именем %s уже существует"%request.POST['roach_name']
    return render(request, 'roaches/create_roach.html',{'errors':error, 'form':form})
    
@login_required
def choose_opponent(request, roach_id):
    error = None
    if request.method == 'POST':
        roach = Roach.objects.get(id = request.POST['id'])
        while True:
            roaches = Roach.objects.all().exclude(id = request.POST['id'])
            opponent = roaches[random.randint(0,len(roaches)-1)]
            if opponent.power < (opponent.level.max_power/2): regenerate_roach(opponent)
            if opponent.power > (opponent.level.max_power/2): break
        return render(request, 'roaches/race_manager.html',{'error':error,'opponent':opponent, 'roach':roach})
    else:
        roach = Roach.objects.get(id = roach_id)
        if roach.power < (roach.level.max_power/2):
            error = u"Ты ещё не отошел от предыдущей гонки."
            return render(request, 'roaches/main.html',{'error':error, 'roach':roach})
        elif roach.status == Status.objects.get(status_name = "free"):
            while True:
                roaches = Roach.objects.all().exclude(id = roach.id)
                opponent = roaches[random.randint(0,len(roaches)-1)]
                if opponent.power < (opponent.level.max_power/2): regenerate_roach(opponent)
                if opponent.power > (opponent.level.max_power/2): break
            return render(request, 'roaches/race_manager.html', {'errors':error,'opponent':opponent, 'roach':roach})
        else:
            temp = what_are_doing(roach)
            return render(request, 'roaches/main.html', {'error':temp[1]['mes'], 'roach':roach,temp[1]['val']: True, 
                                                    'hours': temp[0]['hours'], 'minutes':temp[0]['minutes'], 'seconds':temp[0]['seconds']})

def clars(roach_1, roach_2):
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


@login_required
def create_race(request):
    if request.method == 'POST':
        roach_1 = Roach.objects.get(id = request.POST['my_id'])
        roach_2 = Roach.objects.get(id = request.POST['id'])
        race_id = clars(roach_1, roach_2)
        return view_race(request, race_id, roach_1.id)
    return HttpResponseRedirect('/game/')


@login_required
def work_for_food(request, roach_id):
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
        return render(request, 'main/main.html',{'error':temp[1]['mes'], 'roach':roach,temp[1]['val']: True, 
                                                    'hours': temp[0]['hours'], 'minutes':temp[0]['minutes'], 'seconds':temp[0]['seconds']})
    return render(request, 'main/work.html', {'roach':roach,'form':form})

@login_required
def work_abort(request, roach_id):
    roach = Roach.objects.get(id = roach_id)
    roach.status = Status.objects.get(status_name = "free")
    roach.temp_money = 0
    roach.save()
    return render(request, 'main/main.html',{'roach':roach})
    
@login_required
def train(request, roach_id):
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
        return render(request, 'main/main.html',{'error':temp[1]['mes'], 'roach':roach,temp[1]['val']: True, 
                                                    'hours': temp[0]['hours'], 'minutes':temp[0]['minutes'], 'seconds':temp[0]['seconds']})
    return render(request, 'main/train.html', {'roach':roach,'form':form})

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
    return render(request, 'roaches/main.html',{'roach':roach})
@login_required 
def view_race(request, race_id, roach_id):
    #print log[0]["winner"]
    race = Race.objects.get(id = race_id)
    roach = Roach.objects.get(id = roach_id)
    winner = Roach.objects.get(id = race.winner)
    prize = race.prize
    roach_2 = race.roaches.all().exclude(id = roach.id)[0]
    exec(compile('log='+race.log, '<string>', 'exec'))
    return render(request, 'roaches/race_result.html',{'roach':roach, 'prize':prize, 'winner':winner, 'opponent':roach_2, 'log':log})

@login_required 
def view_stats(request, roach_id):
    roach = Roach.objects.get(id = roach_id)
    roaches = Roach.objects.order_by('-exp_all')[:5]
    return render(request, 'roaches/stat.html',{'roach':roach, 'roaches':roaches})

@login_required 
def evolution(request, roach_id):
    roach = Roach.objects.get(id = roach_id)
    return render(request, 'roaches/evolution.html',{'roach':roach})
