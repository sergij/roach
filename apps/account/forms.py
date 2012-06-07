# -*- coding: utf-8 -*-

from datetime import datetime

from django.conf import settings
from django import forms
from django.utils.translation import ugettext_lazy as _
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.contrib.sites.models import Site

from registration.models import SHA1_RE, RegistrationProfile
from models import ChangeEmailRequest


class ActivationForm(forms.Form):
    activation_key = forms.RegexField(regex=SHA1_RE,
                                max_length=40,
                                label=_(u"Код активации"),
                                error_messages={'invalid': _(u"Некорректный код активации. Проверьте, пожалуйста, правильность ввода.")})

    def clean_activation_key(self):
        try:
            rp = RegistrationProfile.objects.get(activation_key=self.cleaned_data['activation_key'])
        except RegistrationProfile.DoesNotExist:
            raise forms.ValidationError(_(u"Неправильный код активации. Проверьте, пожалуйста, правильность ввода."))
        if rp.activation_key_expired():
            raise forms.ValidationError(_(u"Срок действия активационного кода истёк."))
        return self.cleaned_data['activation_key']


class EmailChangeValidationForm(forms.Form):
    validation_key = forms.RegexField(regex=SHA1_RE, max_length=40,
        label=_(u"Проверочный код"),
        error_messages={'invalid': _(u"Некорректный проверочный код. Проверьте, пожалуйста, правильность ввода.")})

    def clean_validation_key(self):
        try:
            req = ChangeEmailRequest.objects.get(validation_key=self.cleaned_data['validation_key'])
            if req.expired_at < datetime.now():
                raise forms.ValidationError(_(u"Запрос на изменение адреса устарел. Повторите запрос ещё раз, пожалуйста."))
        except ChangeEmailRequest.DoesNotExist:
            raise forms.ValidationError(_(u"Неправильный проверочный код. Проверьте, пожалуйста, правильность ввода."))
        return self.cleaned_data['validation_key']



class EmailChangeForm(forms.Form):
    email = forms.EmailField(label=_("E-mail"), max_length=75)

    def __init__(self, user, *args, **kwargs):
        self.user = user
        super(EmailChangeForm, self).__init__(*args, **kwargs)


    def save(self, site=None, from_email=None):
        email = self.cleaned_data['email']
        req = ChangeEmailRequest.objects.create_request(self.user, email)

        site = site or Site.objects.get_current()

        ctx_dict = {'validation_key': req.validation_key,
                    'expired_at': req.expired_at,
                    'site': site}

        subject = render_to_string('account/email_change_subject.txt', ctx_dict)
        subject = ''.join(subject.splitlines())

        message = render_to_string('account/email_change_text.txt', ctx_dict)

        from_email = from_email or settings.DEFAULT_FROM_EMAIL

        send_mail(subject, message, from_email, [email])

