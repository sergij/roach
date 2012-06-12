# -*- coding: utf-8 -*-

from django.shortcuts import render, redirect

from registration.forms import RegistrationFormUniqueEmail
from registration.backends.default import DefaultBackend as RegistrationBackend
from django.conf import settings
from django.core.urlresolvers import reverse
from django.contrib.auth.models import User
from django.contrib import auth
from django.contrib.auth import REDIRECT_FIELD_NAME
from django.contrib.auth.forms import AuthenticationForm, PasswordResetForm, SetPasswordForm
from django.contrib.auth.tokens import default_token_generator
from django.contrib import messages
from django.utils.translation import ugettext_lazy as _
from django.views.decorators.cache import never_cache
from django.views.decorators.csrf import csrf_protect, csrf_exempt
from django.utils.http import base36_to_int

from forms import ActivationForm, EmailChangeValidationForm
from lib.utils import AjaxFormResponse, SuccessAjaxFormResponse, render_template
from lib.json import model_to_dict, JsonResponse

from models import ChangeEmailRequest

DEFAULT_ACTIVATE_REDIRECT_URL = '/'


def render_popup(request, template, context):
    html = render_template(request, template, context)
    return AjaxFormResponse(request, html=html)


@never_cache
@csrf_protect
def login(request):
    form = AuthenticationForm(data=request.POST or None)
    if form.is_valid():
        user = form.get_user()
        auth.login(request, user)
        next_page = request.POST.get(REDIRECT_FIELD_NAME, '')

        if not request.POST.get('remember_me', None):
            request.session.set_expiry(0)

        if request.is_ajax():
            user_dict = model_to_dict(user, exclude=['password'])
            data = [user_dict]
            if next_page: data[1].update({'next_url': next_page})
            return SuccessAjaxFormResponse(request,
                                           type='loggedIn', data=data)
        else:
            return redirect(next_page or settings.LOGIN_REDIRECT_URL)

    if request.is_ajax():
        context = {
            'base': 'base_form.html',
            'form_url': reverse('account_login'),
            'form': form
        }
        if REDIRECT_FIELD_NAME in request.REQUEST:
            data = request.POST if request.method == 'POST' else request.GET
            context.update({'next': data.get(REDIRECT_FIELD_NAME, '')})
        return render_popup(request, 'account/login.html', context)
    else:
        context = {
            'base': 'base.html',
            'form': form
        }
        if REDIRECT_FIELD_NAME in request.REQUEST:
            data = request.POST if request.method == 'POST' else request.GET
            context.update({'next': data.get(REDIRECT_FIELD_NAME, '')})

        return render(request, 'account/login.html', context)


@csrf_exempt
def logout(request, next_page='/'):
    auth.logout(request)
    if request.is_ajax():
        return JsonResponse({'success': True, 'type': 'loggedOut', 'data': {}})
    else:
        next_page = request.GET.get(REDIRECT_FIELD_NAME, next_page)
        return redirect(next_page)


def register(request):
    form = RegistrationFormUniqueEmail(request.POST or None)
    if form.is_valid():
        reg_backend = RegistrationBackend()
        user = reg_backend.register(request, **form.cleaned_data)
        user.is_active = True
        user.save()
        next_page = request.GET.get(REDIRECT_FIELD_NAME, 'account_login')
        return redirect(next_page)

    if request.is_ajax():
        return render_popup(request, 'account/register.html', {
            'base': 'base_form.html',
            'form_url': reverse('account_register'),
            'form': form
        })
    else:
        return render(request, 'account/register.html', {
            'base': 'base.html',
            'form': form
        })


@never_cache
def activate(request):
    form = ActivationForm(request.GET or None)
    if form.is_valid():
        activation_key = form.cleaned_data['activation_key']
        reg_backend = RegistrationBackend()
        user = reg_backend.activate(request, activation_key)

        if not hasattr(user, 'backend'):
            user.backend='django.contrib.auth.backends.ModelBackend'
        auth.login(request, user)

        try:
            redirect_url = settings.ACTIVATE_REDIRECT_URL
        except AttributeError:
            redirect_url = DEFAULT_ACTIVATE_REDIRECT_URL

        if request.is_ajax():
            return SuccessAjaxFormResponse(request,
                                           type='user', data={'id': user.id})
        else:
            return redirect(redirect_url)

    if request.is_ajax():
        return render_popup(request, 'account/activate.html', {
            'base': 'base_form.html',
            'form_url': reverse('account_activate'),
            'form': form
        })
    else:
        return render(request, 'account/activate.html', {
            'base': 'base.html',
            'form': form
        })


@never_cache
def changeemail(request):
    form = EmailChangeValidationForm(request.GET or None)
    if form.is_valid():
        validation_key = form.cleaned_data['validation_key']

        req = ChangeEmailRequest.objects.get(validation_key=validation_key)
        req.user.email = req.email
        req.user.save()
        req.delete()

        messages.success(request, _(u'Адрес электронной почты успешно установлен'))
        return redirect('/')

    return render(request, 'account/changeemail.html', {
        'form': form
    })



def password_reset(request,
                   email_template_name='account/password_reset_email.html',
                   from_email=None):
    form = PasswordResetForm(request.POST or None)
    if form.is_valid():
        opts = {
            'use_https': request.is_secure(),
            'token_generator': default_token_generator,
            'from_email': from_email,
            'email_template_name': email_template_name,
            'request': request,
        }
        form.save(**opts)
        return SuccessAjaxFormResponse(request, type='user', data={})
    return render_popup(request, 'account/password_reset.html', {
        'base': 'base_form.html',
        'form_url': reverse('account_password_reset'),
        'form': form
    })


def password_reset_confirm(request, uidb36=None, token=None):
    token_generator = default_token_generator
    try:
        uid_int = base36_to_int(uidb36)
        user = User.objects.get(id=uid_int)
    except (ValueError, User.DoesNotExist):
        user = None

    if user is not None and token_generator.check_token(user, token):
        validlink = True
        if request.method == 'POST':
            form = SetPasswordForm(user, request.POST)
            if form.is_valid():
                form.save()
                messages.success(request, _(u'Пароль изменён'))
                return redirect('/')
        else:
            form = SetPasswordForm(None)
    else:
        validlink = False
        form = None
    context = {
        'form': form,
        'validlink': validlink,
    }

    return render(request, 'account/password_reset_confirm.html', context)
