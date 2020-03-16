import csv #used for manipulating csv files
from models import OrbitPath, NearEarthObject


class NEODatabase(object):
    """
    Object to hold Near Earth Objects and their orbits.
    To support optimized date searching, a dict mapping of all orbit date paths to the Near Earth Objects
    recorded on a given day is maintained. Additionally, all unique instances of a Near Earth Object
    are contained in a dict mapping the Near Earth Object name to the NearEarthObject instance.
    """

    def __init__(self, filename):
        """
        :param filename: str representing the pathway of the filename containing the Near Earth Object data
        """
        # TODO: What data structures will be needed to store the NearEarthObjects and OrbitPaths?
        # TODO: Add relevant instance variables for this.
        
        self.filename = filename
        self.neo_name_map = {}
        self.path_date_map = {}

    def load_data(self, filename=None):
        """
        Loads data from a .csv file, instantiating Near Earth Objects and their OrbitPaths by:
           - Storing a dict of orbit date to list of NearEarthObject instances
           - Storing a dict of the Near Earth Object name to the single instance of NearEarthObject
        :param filename:
        :return:
        """

        if not (filename or self.filename):
            raise Exception('Cannot load data, no filename provided')

        filename = filename or self.filename

        # TODO: Load data from csv file.
        # TODO: Where will the data be stored?

        with open(filename, mode='r') as csv_file:

            csv_reader = csv.DictReader(csv_file)

            count_line = 0

            for row in csv_reader:
                if count_line == 0:
                    count_line = 1
                    continue
                orbit_path = OrbitPath(**row)
                if not self.neo_name_map.get(row['name'], None):
                    self.neo_name_map[row['name']] = NearEarthObject(**row)

                near_earth_object = self.neo_name_map.get(row['name'], None)
                near_earth_object.update_orbits(orbit_path)

                if not self.path_date_map.get(row['close_approach_date'], None):
                    self.path_date_map[row['close_approach_date']] = []

                self.path_date_map[row['close_approach_date']].append(near_earth_object)
        
        #return None