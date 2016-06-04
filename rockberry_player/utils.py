from __future__ import unicode_literals
from functools import wraps
from kivy.clock import Clock


def MopidyRef(item):

    if not item:
        return None

    if '__model__' not in item:
        print 'item %r is not a Mopidy Model' % item

    #assert '__model__' in item, 'item %r is not a Mopidy Model' % item

    return {'__model__': 'Ref',
            'type': item.get('__model__'),
            'name': item.get('name'),
            'uri': item.get('uri')}


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
        self._args = args
        self._kwargs = kwargs
        self._trigger()


# TODO: Catch exceptions and raise with better information
@scheduled
def set_property(instance, prop_name, value):
    instance.property(prop_name).set(instance, value)
    # logger.debug('[%r] Property %s = %r', instance, prop_name, value)


def assign_property(instance, prop_name, field=None, get_data=None):

    if field is None:
        field = prop_name

    def _get_data(data):
        if len(data) == 1:
            return data.values()[0]
        else:
            return data.get(field)

    if get_data is None:
        get_data = _get_data

    def cb_set_property(*args, **kwargs):
        if args:
            value = get_data({i: arg for i, arg in enumerate(args)})
        else:
            value = get_data(kwargs)

        set_property(instance, prop_name, value)

    return cb_set_property