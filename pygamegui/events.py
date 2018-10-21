from inspect import signature


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

    def subscribe(self, handler: callable(None), predicate: any):
        """ Subscribes the given handler to events filtered by the given predicate.
        The `predicate` argument can also be the event code. """
        self.__listeners.insert(0, (Predicate(predicate), Handler(handler)))

    def dispatch(self, event):
        """ Dispatches all the given events to the appropriate subscribed listeners """
        for listener in self.__listeners:
            if listener[0].test(event):
                listener[1].handle(event)


events = Dispatcher()
""" Stores the singleton instance of the Dispatcher class """

__next_event_code = 128


def event_code() -> int:
    """ Returns an event code that is ensured to be unique """
    global __next_event_code
    __next_event_code += 1
    return __next_event_code - 1

