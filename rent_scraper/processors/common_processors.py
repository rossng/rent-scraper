import re
from future.utils import lmap, lfilter

class TextSearch(object):

    def __init__(self, search_phrase):
        self.search_phrase = search_phrase.lower()

    def __call__(self, values):
        """Takes a list of property features and determines whether it contains the phrase that the AbodeTextSearch
        object was initialised with. Case insensitive."""
        return any(self.search_phrase in s.lower() for s in values)