# -*- coding: utf-8 -*-
from django import forms
from roaches.models import BaseSkillType, Level, Roach

class WorkingForm(forms.Form):
    hours = forms.ChoiceField(label=u"Сколько часов собираешся проработать?",choices = ([('1','1 час'), ('2','2 часа'), ('3','3 часa'),('4','4 часa'),('5','5 часов'),('6','6 часов'),('7','7 часов'),('8','8 часов'),]), initial='1',)

class TrainingForm(forms.Form):
    hours = forms.ChoiceField(label=u"Сколько часов собираешся пропотеть?",choices = ([('1','1 час'), ('2','2 часа'), ('3','3 часa'),('4','4 часa'),('5','5 часов'),('6','6 часов'),('7','7 часов'),('8','8 часов'),]), initial='1',)

class RoachForm(forms.ModelForm):
    sex = forms.ChoiceField(label=u'Пол таракана',choices = ([('1','Mуж.'), ('0','Жен.'), ]), initial='1',)
    base_skill_type = forms.ModelChoiceField(label=u'Специализация таракана',queryset=BaseSkillType.objects.all(),initial='1') 
    class Meta:
        model = Roach
        fields = ('nick',)

class ChooseOpponent(forms.Form):
    level = forms.ModelChoiceField(label=u'Сила противника',queryset=Level.objects.all(), initial='0',)
        
class DaysForm(forms.Form):
    #days = forms.Text(label=u"Период в днях")
    pass
    