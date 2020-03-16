class NearEarthObject(object):
    """
    Object containing data describing a Near Earth Object and it's orbits.
    # TODO: You may be adding instance methods to NearEarthObject to help you implement search and output data.
    """

    def __init__(self, **kwargs):
        """
        :param kwargs:    dict of attributes about a given Near Earth Object, only a subset of attributes used
        """
        # TODO: What instance variables will be useful for storing on the Near Earth Object?
        
        self.id = kwargs.get('id', None)
        self.name = kwargs.get('name', 'no name')

        self.diameter_min_km = float(kwargs.get('estimated_diameter_min_kilometers', 0))
        self.is_potentially_hazardous_asteroid = kwargs.get('is_potentially_hazardous_asteroid', False)
        
        self.orbits = []#Orbits

    def update_orbits(self, orbit):
        """
        Adds an orbit path information to a Near Earth Object list of orbits
        :param orbit: OrbitPath
        :return: None
        """

        # TODO: How do we connect orbits back to the Near Earth Object?
        
        self.orbits.append(orbit)

    def __str__(self):
        """
        Returns info about the object
        """

        return 'NearEarthObject id:{} name:{} orbit_dates:{} harzardous_asteriod:{}'.format(self.id,
                                                                                            self.name,
                                                                                            [orbit.close_approach_date for orbit in self.orbits],
                                                                                            self.is_potentially_hazardous_asteroid)
    
    def __repr__(self):
        """
        Returns info about the object for debugging purposes
        """

        return 'NearEarthObject id:{} name:{} orbit_dates:{} harzardous_asteriod:{}'.format(self.id,
                                                                                            self.name,
                                                                                            [orbit.close_approach_date for orbit in self.orbits],
                                                                                            self.is_potentially_hazardous_asteroid)


class OrbitPath(object):
    """
    Object containing data describing a Near Earth Object orbit.
    # TODO: You may be adding instance methods to OrbitPath to help you implement search and output data.
    """

    def __init__(self, **kwargs):
        """
        :param kwargs:    dict of attributes about a given orbit, only a subset of attributes used
        """
        # TODO: What instance variables will be useful for storing on the Near Earth Object?
        self.neo_name = kwargs.get('name', 'no name')
        self.miss_distance_kilometers = float(kwargs.get('miss_distance_kilometers', 0))
        self.close_approach_date = kwargs.get('close_approach_date', None)

    def __str__(self):
        """
        Returns info about the object
        """

        return 'OrbitPath neo_name:{} close_approach_date:{} missed_distance_kilometers:{}'.format(self.neo_name,
                                                                                                   self.close_approach_date,
                                                                                                   self.miss_distance_kilometers)
