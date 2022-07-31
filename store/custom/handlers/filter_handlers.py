from abc import ABC, abstractmethod

from .string_handlers import string_to_dictionary


class FilterHandler(ABC):

    _data = None

    @abstractmethod
    def _handle_filter(self):
        pass

    def transform_filter(self, data):
        self._data = data
        self._handle_filter()
        filter = self._filter
        return filter


class FeaturesFilterHandler(FilterHandler):

    def _handle_filter(self):
        data = string_to_dictionary(self._data)
        self._filter = {f'features__{key}__in': item for key, item in data.items()}


class SearchFilterHandler(FilterHandler):

    def _handle_filter(self):
        self._filter = {'name__icontains': self._data}


feature_filter_handler = FeaturesFilterHandler()
search_filter_handler = SearchFilterHandler()


filter_keyword_dictionary = {
    'filters': feature_filter_handler,
    'search': search_filter_handler,
}
