from __future__ import unicode_literals
from functools import partial, wraps
from kivy.clock import Clock

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

    def scheduled(_function_):

        def cb_function(*args, **kwargs):
            @wraps(_function_)
            def do_function(*args, **kwargs):
                return _function_(*args, **kwargs)

            # Remove dt parameter (last 'args' item)
            args = tuple(list(args)[:-1])
            # Call the function
            do_function(*args, **kwargs)

        @wraps(_function_)
        def schedule_function(*args, **kwargs):
            Clock.unschedule(cb_function)
            Clock.schedule_once(
                partial(cb_function, *args, **kwargs),
                timeout=timeout)

        return schedule_function

    return scheduled
