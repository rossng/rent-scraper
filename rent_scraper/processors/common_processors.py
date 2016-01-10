import re

from future.moves import itertools
from future.utils import lmap, lfilter
from scrapy.loader import wrap_loader_context
from scrapy.utils.datatypes import MergeDict


class TextSearch(object):

    def __init__(self, search_phrase):
        self.search_phrase = search_phrase.lower()

    def __call__(self, values):
        """Takes a list of property features and determines whether it contains the phrase that the AbodeTextSearch
        object was initialised with. Case insensitive."""
        return any(self.search_phrase in s.lower() for s in values)

class Concatenate(object):

    def __init__(self, *functions, **default_loader_context):
        self.functions = functions
        self.stop_on_none = default_loader_context.get('stop_on_none', True)
        self.default_loader_context = default_loader_context

    def __call__(self, value, loader_context=None):
        if loader_context:
            context = MergeDict(loader_context, self.default_loader_context)
        else:
            context = self.default_loader_context
        wrapped_funcs = [wrap_loader_context(f, context) for f in self.functions]

        results = []

        for func in wrapped_funcs:
            #if value is None and self.stop_on_none:
            #    break
            results.append(func(value))

        return list(itertools.chain(*results))