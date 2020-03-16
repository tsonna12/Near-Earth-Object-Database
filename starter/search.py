from collections import namedtuple, defaultdict
from enum import Enum

import operator

from exceptions import UnsupportedFeature
from models import NearEarthObject, OrbitPath


class DateSearch(Enum):
    """
    Enum representing supported date search on Near Earth Objects.
    """
    between = 'between'
    equals = 'equals'

    @staticmethod
    def list():
        """
        :return: list of string representations of DateSearchType enums
        """
        return list(map(lambda output: output.value, DateSearch))


class Query(object):
    """
    Object representing the desired search query operation to build. The Query uses the Selectors
    to structure the query information into a format the NEOSearcher can use for date search.
    """

    Selectors = namedtuple('Selectors', ['date_search', 'number', 'filters', 'return_object'])
    DateSearch = namedtuple('DateSearch', ['type', 'values'])
    ReturnObjects = {'NEO': NearEarthObject, 'Path': OrbitPath}

    def __init__(self, **kwargs):
        """
        :param kwargs: dict of search query parameters to determine which SearchOperation query to use
        """
        # TODO: What instance variables will be useful for storing on the Query object?
        
        self.date = kwargs.get('date', None)
        self.end_date = kwargs.get('end_date', None)

        self.filter = kwargs.get('filter', None)
        self.number = kwargs.get('number', None)

        self.start_date = kwargs.get('start_date', None)
        self.return_object = kwargs.get('return_object', None)

    def build_query(self):
        """
        Transforms the provided query options, set upon initialization, into a set of Selectors that the NEOSearcher
        can use to perform the appropriate search functionality
        :return: QueryBuild.Selectors namedtuple that translates the dict of query options into a SearchOperation
        """

        
        # TODO: Translate the query parameters into a QueryBuild.Selectors object
       
        search_date = Query.DateSearch(DateSearch.equals.name, self.date) if self.date else Query.DateSearch(DateSearch.between.name, [self.start_date, self.end_date])
        object_to_return = Query.ReturnObjects.get(self.return_object)

        filters=[]
        
        if self.filter:
            options = Filter.create_filter_options(self.filter)
            
            for key, val in options.items():
                for a_filter in val:

                    option = a_filter.split(':')[0]

                    operation = a_filter.split(':')[1]

                    value = a_filter.split(':')[-1]

                    filters.append(Filter(option, key, operation, value))

        return Query.Selectors(search_date, self.number, filters, object_to_return)


class Filter(object):
    """
    Object representing optional filter options to be used in the date search for Near Earth Objects.
    Each filter is one of Filter.Operators provided with a field to filter on a value.
    """
    Options = {
        # TODO: Create a dict of filter name to the NearEarthObject or OrbitalPath property
        'diameter': 'diameter_min_km',
        'distance': 'miss_distance_kilometers',
        'is_hazardous': 'is_potentially_hazardous_asteroid'
    }

    Operators = {
        # TODO: Create a dict of operator symbol to an Operators method, see README Task 3 for hint
        '>=': operator.ge,
        '=': operator.eq,
        '>': operator.gt
    }

    def __init__(self, field, object, operation, value):
        """
        :param field:  str representing field to filter on
        :param field:  str representing object to filter on
        :param operation: str representing filter operation to perform
        :param value: str representing value to filter for
        """
        self.field = field
        self.object = object
        self.operation = operation
        self.value = value

    @staticmethod
    def create_filter_options(filter_options):
        """
        Class function that transforms filter options raw input into filters
        :param input: list in format ["filter_option:operation:value_of_option", ...]
        :return: defaultdict with key of NearEarthObject or OrbitPath and value of empty list or list of Filters
        """

        # TODO: return a defaultdict of filters with key of NearEarthObject or OrbitPath and value of empty list or list of Filters
        
        value_to_return = defaultdict(list)

        for filter_option in filter_options:
            fil = filter_option.split(':')[0]

            if hasattr(NearEarthObject(), Filter.Options.get(fil)):
                value_to_return['NearEarthObject'].append(filter_option)
            elif hasattr(OrbitPath(), Filter.Options.get(fil)):
                value_to_return['OrbitPath'].append(filter_option)

        return value_to_return

    def apply(self, results):
        """
        Function that applies the filter operation onto a set of results
        :param results: List of Near Earth Object results
        :return: filtered list of Near Earth Object results
        """
        # TODO: Takes a list of NearEarthObjects and applies the value of its filter operation to the results
        list_filtered = []

        for near_earth_object in results:
            operation = Filter.Operators.get(self.operation)
            field = Filter.Options.get(self.field)
            value = getattr(near_earth_object, field)

            try:
                if operation(value, self.value):
                    list_filtered.append(near_earth_object)
            except Exception as exp:
                if operation(str(value), str(self.value)):
                    list_filtered.append(near_earth_object)

        return list_filtered

class NEOSearcher(object):
    """
    Object with date search functionality on Near Earth Objects exposed by a generic
    search interface get_objects, which, based on the query specifications, determines
    how to perform the search.
    """

    def __init__(self, db):
        """
        :param db: NEODatabase holding the NearEarthObject instances and their OrbitPath instances
        """
        self.db = db
        # TODO: What kind of an instance variable can we use to connect DateSearch to how we do search?
        self.path_date_map = dict(db.path_date_map)

        self.date_search_type = None

    def get_objects(self, query):
        """
        Generic search interface that, depending on the details in the QueryBuilder (query) calls the
        appropriate instance search function, then applys any filters, with distance as the last filter.
        Once any filters provided are applied, return the number of requested objects in the query.return_object
        specified.
        :param query: Query.Selectors object with query information
        :return: Dataset of NearEarthObjects or OrbitalPaths
        """
        # TODO: This is a generic method that will need to understand, using DateSearch, how to implement search
        # TODO: Write instance methods that get_objects can use to implement the two types of DateSearch your project
        # TODO: needs to support that then your filters can be applied to. Remember to return the number specified in
        # TODO: the Query.Selectors as well as in the return_type from Query.Selectors
        
        self.date_search_type = query.date_search.type
        date = query.date_search.values
        
        all_neos = []

        if self.date_search_type == DateSearch.equals.name:
            all_neos = self.date_search_equal(self.path_date_map, date)
        elif self.date_search_type == DateSearch.between.name:
            all_neos = self.date_search_between(self.path_date_map, date[0], date[1])

        distance_filter = None
        for fil in query.filters:
            if fil.field == 'distance':
                distance_filter = fil
                continue
            all_neos = fil.apply(all_neos)
        orbits = self.get_orbit_paths_from_neos(all_neos)

        filtered_orbits = orbits
        filtered_neos = all_neos

        if distance_filter:
            filtered_orbits = distance_filter.apply(orbits)

            filtered_neos = self.get_neo_from_orbit_path(filtered_orbits)

        filtered_neos = list(set(filtered_neos))
        filtered_orbits = list(set(filtered_orbits))

        if query.return_object == OrbitPath:
            return filtered_orbits[: int(query.number)]
        return filtered_neos[: int(query.number)]
    
    
    
    def get_orbit_paths_from_neos(self, all_neos):
        paths = []
        for neo in all_neos:
            paths += neo.orbits
        return paths

    def get_neo_from_orbit_path(self, orbit_paths):
        neo = [self.db.neo_name_map.get(path.neo_name) for path in orbit_paths]
        return neo

    def date_search_between(self, orbit_path, start_date, end_date):
        all_neos = []
        for key, value in orbit_path.items():
            if key >= start_date and key <= end_date:
                all_neos += value
        return all_neos

    def date_search_equal(self, orbit_path, date):
        all_neos = []
        for key, value in orbit_path.items():
            if key == date:
                all_neos += value
        return all_neos
