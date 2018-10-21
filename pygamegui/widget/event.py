from pygamegui.events import event_code


WIDGET_MOUSE_DOWN = event_code()
""" When any mouse button is pressed while a widget is hovered """
WIDGET_MOUSE_UP = event_code()
""" When any mouse button is released while a widget is hovered """
WIDGET_HOVER_ENTER = event_code()
""" When the mouse cursor enters a widget's rect  """
WIDGET_HOVER_EXIT = event_code()
""" When the mouse cursor leaves a widget's rect  """


class WidgetEvent:
    """ An event regarding a widget """
    def __init__(self, widget, code: int):
        self.widget = widget
        """ The widget being the source of this event """
        self.type = code
        """ Type of this event """


class WidgetMouseButtonEvent(WidgetEvent):
    """ A widget event that occurs when a mouse button is pressed or released
    (or the mouse wheel rotated) when the widget is hovered """
    def __init__(self, widget, code: int, button: int):
        super(__class__, self).__init__(widget, code)
        self.button = button
        """ Code associated with the button that has been pressed or released during this event.
        See `pygamegui.mouse_buttons` """
