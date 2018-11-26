from inspect import signature


class Event:
    """ Base class for all event types """

    def __init__(self, code: int):
        """ Constructs an event with the given integer code representing its type """
        self.type = code
        """ The type/code of this event """


class Handler:
    """ Subscribed to events using a dispatcher handles events """

    def __init__(self, handler: callable(None)):
        self.__handler = handler

    def handle(self, event):
        """ Handles the given event """
        num_params = len(signature(self.__handler).parameters)
        if num_params == 0:
            return self.__handler()
        else:
            return self.__handler(event)


class Predicate:
    """ Filters events """

    def __init__(self, predicate: any):
        if callable(predicate):
            self.__predicate = predicate
        elif type(predicate) == int:
            self.__predicate = lambda event: event.type == predicate
        elif predicate is None:
            self.__predicate = lambda event: True
        else:
            self.__predicate = lambda event: False

    def test(self, event):
        """ Tests the given event """
        return self.__predicate(event)


class Dispatcher:
    """ Does event dispatching """

    def __init__(self):
        self.__listeners = []

    def subscribe(self, predicate: any, handler: callable(None)):
        """ Subscribes the given handler to events filtered by the given predicate.
        The `predicate` argument can also be an event code. """
        self.__listeners.insert(0, (Predicate(predicate), Handler(handler)))

    def dispatch(self, event):
        """ Dispatches all the given events to the appropriate subscribed listeners """
        for listener in self.__listeners:
            if listener[0].test(event):
                listener[1].handle(event)

    def on(self, predicate: any):
        """ Returns a decorator that will subscribe any function its applied on
        to events filtered by the given predicate. The `predicate` argument can also be an event code. """
        def decorator(f):
            self.subscribe(predicate, f)
            return f
        return decorator


events = Dispatcher()
""" Stores the singleton instance of the Dispatcher class """


class EventCode:
    """ Generates unique event codes """

    def __init__(self, start: int = 0):
        self.__last_event_code = start - 1

    def __call__(self, *args, **kwargs):
        """ Generates and returns a unique event code """
        self.__last_event_code += 1
        return self.__last_event_code


event_code = EventCode(128)
""" Stores the singleton instance of the EventCode class used to generate event codes.
Call this object to obtain a unique event code. """
