from __future__ import unicode_literals
from functools import partial, wraps
from kivy.clock import Clock
from datetime import timedelta, datetime as dt

from .debug import debug_function


def MarkupText(text, **fmt_options):

    def add_markup_tag(text='', tag='', value=False):
        if value is True:
            return '[{tag}]{text}[/{tag}]'.format(tag=tag, text=text)
        elif value is False:
            return text
        else:
            return '[{tag}={value}]{text}[/{tag}]'.format(text=text,
                                                          tag=tag,
                                                          value=value)
    if not text:
        return ''

    markup_text = text
    for tag, value in fmt_options.iteritems():
        markup_text = add_markup_tag(text=markup_text,
                                     tag=tag,
                                     value=value)
    return markup_text


def delayed(timeout):

    def wrapper_delayed(_function_):

        _args = []
        _kwargs = {}

        def cb_function(dt):
            @wraps(_function_)
            def do_function(*args, **kwargs):
                return _function_(*args, **kwargs)

            # Call the function
            do_function(*tuple(_args), **_kwargs)

        cb_trigger = Clock.create_trigger(cb_function, timeout)

        @wraps(_function_)
        def trigger_function(*args, **kwargs):
            _args[:] = []
            _args.extend(list(args))
            _kwargs.clear()
            _kwargs.update(kwargs)
            cb_trigger()

        return trigger_function

    return wrapper_delayed


def format_timestamp(time, now=None):

    if now is not None:
        elapsed_secs = now - time
        if elapsed_secs < 60:
            return ('Ahora')
        if elapsed_secs < 3600:
            return ('Hace %d minutos' % round(elapsed_secs / 60))
        if elapsed_secs < 3600 * 6:
            return ('Hace %d horas' % round(elapsed_secs / 3600))

        dt_time = dt.fromtimestamp(time)
        dt_now = dt.fromtimestamp(now)

        if dt_time.date() == dt_now.date():
            return 'Hoy %s' % dt_time.strftime('%H:%M')
        if dt_time.date() == dt_now.date() - timedelta(days=1):
            return 'Ayer %s' % dt_time.strftime('%H:%M')

    return dt_time.strftime('%d-%b %H:%M')

