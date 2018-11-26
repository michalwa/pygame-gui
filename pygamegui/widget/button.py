from .widget import Widget
from .group import WidgetGroup, default_group
from .event import WidgetEvent, WIDGET_MOUSE_DOWN, WIDGET_MOUSE_UP, WIDGET_HOVER_EXIT
from ..events import event_code


BUTTON_CLICKED = event_code()
""" When a button gets clicked """


class ButtonClickedEvent(WidgetEvent):
    """ When a button gets clicked """

    def __init__(self, widget, button: int):
        super(__class__, self).__init__(widget, BUTTON_CLICKED)
        self.button = button
        """ The mouse button that the button widget was clicked with """


class Button(Widget):
    """ A button widget """

    def __init__(self, rect, group: WidgetGroup = default_group):
        super(__class__, self).__init__(rect, group)

        self.__click_buttons = []

        self.subscribe(WIDGET_MOUSE_DOWN, self.__button_on_mouse_down)
        self.subscribe(WIDGET_MOUSE_UP, self.__button_on_mouse_up)
        self.subscribe(WIDGET_HOVER_EXIT, self.__button_on_hover_exit)

    def __button_on_mouse_down(self, event):
        self.__click_buttons.append(event.button)

    def __button_on_mouse_up(self, event):
        if event.button in self.__click_buttons:
            self.dispatch(ButtonClickedEvent(self, event.button))
        self.__click_buttons.remove(event.button)

    def __button_on_hover_exit(self):
        self.__click_buttons.clear()
