import os


def load_config():
    db_uri = os.getenv('DB_URI')
    if db_uri is None or len(db_uri) == 0:
        raise ValueError("DB_URI invalid")

    return {'DB_URI': db_uri}
