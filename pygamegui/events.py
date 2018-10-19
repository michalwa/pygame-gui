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
        elif predicate is None:
            self.__predicate = lambda _: True
        else:
            self.__predicate = lambda _: False

    def test(self, event):
        """ Tests the given event """
        return self.__predicate(event)


class Dispatcher:
    """ Does event dispatching """
    def __init__(self):
        self.__listeners = []

    def subscribe(self, handler: callable(None), predicate: any):
        p = None
        if predicate is None:
            p = Predicate()
        elif callable(predicate):
            p = Predicate(predicate)
        elif type(predicate) == int:
            p = Predicate(lambda evt: evt.type == predicate)

        self.__listeners.insert(0, (p, Handler(handler)))

    def dispatch(self, event):
        """ Dispatches all the given events to the appropriate subscribed listeners """
        for listener in self.__listeners:
            if listener[0].test(event):
                listener[1].handle(event)


events = Dispatcher()
""" Stores the singleton instance of the Dispatcher class """
