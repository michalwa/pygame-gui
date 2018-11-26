class Updater:
    """ Updates stuff """

    def __init__(self):
        self.__listeners = []

    def add(self, listener: callable):
        """ Adds a listener to update """
        self.__listeners.append(listener)

    def update(self):
        """ Calls all update listeners """
        for listener in self.__listeners:
            listener()


updater = Updater()
