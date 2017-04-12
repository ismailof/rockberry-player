from kivy.logger import Logger
from kivy.event import EventDispatcher
from kivy.properties import StringProperty, \
    ListProperty, AliasProperty

from gpio_controls.manager import GpioInputManager


class GpioBehavior(EventDispatcher):
    focus_widgets = {}
    group_widgets = {}

    gpio_group = StringProperty('')

    def has_focus(self):
        return self.focus_widgets[self.gpio_group] == self

    def set_focus(self, value=True):
        self.focus_widgets[self.gpio_group] = self \
            if value else None

    focus = AliasProperty(has_focus, set_focus)

    def __init__(self, *args, **kwargs):
        if not self.group_widgets:
            self.group_widgets.update(dict.fromkeys(GpioInputManager.get_groups(), []))
            self.focus_widgets.update(dict.fromkeys(GpioInputManager.get_groups(), None))
            GpioInputManager.register_callback(self.dispatch_event)
        super(GpioBehavior, self).__init__(*args, **kwargs)

    @classmethod
    def dispatch_event(cls, event_data):
        widget = cls.focus_widgets[event_data['group']]
        Logger.debug(
            "{0} : on_{event}({data}) [gr:'{group}' c:'{control}'] to {1}".format(
                'GPIO Event', widget, **event_data)
            )
        if widget:
            if event_data['data'] is None:
                widget.dispatch('on_' + event_data['event'])
            else:
                widget.dispatch('on_' + event_data['event'],
                                event_data['data'])

    def on_gpio_group(self, instance, group):
        for group in self.group_widgets:
            try:
                self.group_widgets[group].remove(self)
            except ValueError:
                pass
        self.group_widgets[group].append(self)
        if self.focus_widgets[group] is None:
            self.focus = True

    def on_parent(self, instance, parent):
        if parent == None:
            self.group_widgets[self.gpio_group].pop(self)

