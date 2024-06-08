import os
import yaml
import test_schema
from cerberus import Validator


def load_test_files():
    """ Loads test files and constructs object from the yml representation
    """
    query_dir = os.path.join(os.path.dirname(__file__), '..', 'queries')
    test_files = [f for f in os.listdir(query_dir) if f.endswith('.yml')]

    validator = Validator(test_schema.schema)
    test_objects = []

    for test_file in test_files:
        with open(os.path.join(query_dir, test_file), 'r') as file:

            test = yaml.safe_load(file)
            if not validator.validate(test):
                errors = validator.errors
                print(f"Validation errors in {test_file}: {errors}")
                continue

        test_objects.append(test)

    return test_objects
