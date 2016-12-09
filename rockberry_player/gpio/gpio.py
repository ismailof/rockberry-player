import logging

from kivy.event import EventDispatcher
from kivy.properties import NumericProperty, StringProperty, \
    BooleanProperty, ListProperty, AliasProperty

from gpio_controls.inputs import GpioInput

logger = logging.getLogger('gpio_controls')
logger.addHandler(logging.StreamHandler())

class GpioInputProvider(object):
    controls = []
    callbacks = None
    
    @classmethod
    def add_control(cls, control, id=None, group=None):        
        assert isinstance(control, GpioInput), \
            "{} is not an instance of GpioInput".format(control)

        control.on_event = cls.gpio_event        
        control.id = id or control.id or 'gpio_input-{0:02d}'.format(len(cls.controls))
        if group:
            control.group = group
        
        cls.controls.append(control)
        
        logger.debug("Registered Control: {}".format(
            control, control.group))

    @classmethod
    def register_callback(cls, callback):
        #assert group in cls.get_groups(), \
            #"{} is not a registered GPIO Input group".format(group)

        assert callback is None or callable(callback), \
            "{} is not a callable function".format(callback)
        
        cls.callback = callback

    @classmethod
    def gpio_event(cls, control, event=None, data=None):        
        logger.debug( "Event from {}: event='{}'  data={}".format(
            control, control.group, event, data))
        if cls.callback:
            cls.callback({
                'event': event,
                'group': control.group,
                'control': control.id,
                'data': data
                }
            )

    @classmethod
    def get_groups(cls):
        return set(control.group for control in cls.controls)

    @classmethod
    def close(cls):
        for control in cls.controls:
            control.close()


class GpioBehavior(EventDispatcher):
    focus_widgets = {}
    group_widgets = {}
    
    gpio_group = StringProperty('')    
    gpio_inputs = ListProperty([])
    
    def has_focus(self):
        return self.focus_widgets[self.gpio_group] == self
    
    def set_focus(self, value=True):
        self.focus_widgets[self.gpio_group] = self \
            if value else None
    
    focus = AliasProperty(has_focus, set_focus)
    
    def __init__(self, *args, **kwargs):
        if not self.group_widgets:
            self.group_widgets.update(dict.fromkeys(GpioInputProvider.get_groups(), []))
            self.focus_widgets.update(dict.fromkeys(GpioInputProvider.get_groups(), None))
            GpioInputProvider.register_callback(self.dispatch_event)
        super(GpioBehavior, self).__init__(*args, **kwargs)
    
    @classmethod
    def dispatch_event(cls, event_data):
        widget = cls.focus_widgets[event_data['group']]
        if widget:
            widget.dispatch(
                'on_' + event_data['event'], 
                event_data['data'])
        
    def on_gpio_inputs(self, instance, input_types):        
        for control_class in input_types:
            for event in control_class._event_list:
                exec('''def on_{0}(self, *args, **kwargs): pass'''.format(event))
                self.register_event_type('on_' + event)                
    
    def on_gpio_group(self, instance, group):
        for group in self.group_widgets:
            try:
                self.group_widgets[group].remove(self)
            except ValueError:
                pass
        self.group_widgets[group].append(self)
    
    def on_parent(self, instance, parent):
        if parent == None:
            self.group_widgets[self.gpio_group].pop(self)        
        
