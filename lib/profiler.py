# -*- coding: utf-8 -*-
import hotshot
import os
from time import time
import settings
from random import randint

try:
    ENV_ROOT = settings.ENV_ROOT
except:
    ENV_ROOT = "/tmp"

def profile(log_file_prefix):
    """Profile some callable.

    This decorator uses the hotshot profiler to profile some callable (like
    a view function or method) and dumps the profile data somewhere sensible
    for later processing and examination.
    """

    def _outer(func):
        def _inner(*args, **kwargs):
            filename = 'prof-%s-%s-%s.x' % (log_file_prefix, str(time()), randint(3234, 12344))
            logfn = os.path.join(ENV_ROOT, 'log', filename)

            prof = hotshot.Profile(logfn)
            try:
                ret = prof.runcall(func, *args, **kwargs)
            finally:
                prof.close()
            return ret

        return _inner
    return _outer
