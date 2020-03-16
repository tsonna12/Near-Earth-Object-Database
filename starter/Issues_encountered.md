
## Bugs and fixed

 Import error: from models OrbitPath, NearEarthObject

Fixed: from .models import Orbith, NearEarthObject

## Bugs and fixed

Failed test cases

- Bugs: test_find_unique_number_between_dates_with_diameter (tests.test_neo_database.TestNEOSearchUseCases)
AttributeError: 'NearEarthObject' object has no attribute 'diameter_min_km'

- Fixed: Rename attribute in NearEarthObject model to `diameter_min_km`

- Bugs: test_find_unique_number_between_dates_with_diameter_and_hazardous_and_distance (tests.test_neo_database.TestNEOSearchUseCases)

AttributeError: 'OrbitPath' object has no attribute 'neo_name'

- Fixed: Rename an attribute `name` in OrbitPath to `neo_name`