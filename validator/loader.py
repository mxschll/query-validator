import os
import yaml
import schema
from cerberus import Validator


def load_test_files(path):
    """ Loads test files and constructs object from the yml representation
    """

    test_files = [f for f in os.listdir(path) if f.endswith('.yml')]

    validator = Validator(schema.schema)
    test_objects = []

    for test_file in test_files:
        with open(os.path.join(path, test_file), 'r') as file:

            test = yaml.safe_load(file)
            if not validator.validate(test):
                errors = validator.errors
                print(f"Validation errors in {test_file}: {errors}")
                continue

        test_objects.append(test)

    return test_objects
