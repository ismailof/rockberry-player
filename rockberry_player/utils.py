from __future__ import unicode_literals
from functools import wraps
from kivy.clock import Clock


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


def scheduled(_function_):
    @wraps(_function_)
    def do_function(*args, **kwargs):
        return _function_(*args, **kwargs)

    def schedule_function(*args, **kwargs):
        Clock.schedule_once(lambda dt:
                            do_function(*args, **kwargs))
    return schedule_function


class delayed(object):

    def __init__(self, timeout):
        self._trigger = Clock.create_trigger(self.cb_function, timeout)

    def __call__(self, function):
        self._function_ = function
        return self.trigger_function

    def cb_function(self, dt):
        @wraps(self._function_)
        def do_function(*args, **kwargs):
            return self._function_(*args, **kwargs)

        do_function(*self._args, **self._kwargs)

    def trigger_function(self, *args, **kwargs):
        if 'time_position' in kwargs:
            time_position = kwargs.pop('time_position')
        self._args = args
        self._kwargs = kwargs
        self._trigger()


