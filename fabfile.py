# -*- coding: utf-8 -*-
import os
from datetime import datetime
from fabric.api import local, settings, abort, run, sudo, \
                       cd, env, put, path, prefix, runs_once

def development():
    env.stage = 'development'
    env.user = 'serk'
    env.hosts = ['174.133.21.90']

def alwaysdata():
    env.stage = 'development'
    env.user = 'roach'
    env.hosts = ['ssh.alwaysdata.com']

dev = development
alw = alwaysdata

@runs_once
def pack():
    env.datetag = datetime.now().strftime('%Y%m%d-%H%M%S')
    env.packed_filename = env.datetag + '.tgz'
    local("tar czf /tmp/%s --exclude './local_settings.py' --exclude '*.pyc' --exclude-vcs ." % env.packed_filename)

def putcode():
    release_dir = 'releases/%s' % env.datetag
    src_dir = 'src'
    with path('~'):
        put('/tmp/%s' % env.packed_filename, 'tmp/')
        # run('mkdir -p %s' % release_dir)
        # with cd('%s' % release_dir):
        #     run('tar -xzf ~/tmp/%s' % env.packed_filename)
        with cd('%s' % src_dir):
            run('tar -xzf ~/tmp/%s' % env.packed_filename)
        run('rm ~/tmp/%s' % env.packed_filename)
    local("rm /tmp/%s" % env.packed_filename)
    # run('ln -sfT ~/%s/ ~/src' % release_dir)


def update_pip():
    with prefix('source ~/.env/bin/activate'):
        run("pip install 'distribute>=0.6.25'")
        run('pip install -r ~/src/deploy/%s/requirements.txt' % (env.stage))

def configure_project():
    run('cp ~/conf/local_settings.py ~/src')

def setup_project():
    configure_project()
    # update_pip()
    # with prefix('source ~/.env/bin/activate'):
    with cd('~/src'):
        run('python manage.py collectstatic --noinput')
        run('python manage.py syncdb')
        run('python manage.py migrate')

def validate():
    # with prefix('source ~/.env/bin/activate'):
    with cd('~/src'):
        run('python manage.py validate')

def reload_server():
    sudo('/home/%s/reload.sh' % env.user, shell=False)


def deploy():
    make_dirs()
    pack()
    putcode()
    setup_project()
    validate()
    # reload_server()

def make_dirs():
    run('mkdir -p ~/{static,log}')

