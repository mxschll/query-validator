from evarify import ConfigStore, EnvironmentVariable
from evarify.filters.python_basics import validate_is_boolean_true
from dotenv import load_dotenv

# Load environment variables from a .env file (optional)
load_dotenv()

# Define the configuration schema using evarify
settings = ConfigStore({
    'DB_URI': EnvironmentVariable(
        name='DB_URI',
        is_required=True
    ),

    'LOG_LEVEL': EnvironmentVariable(
        name='LOG_LEVEL',
        default_val='INFO',
        is_required=False
    ),
    'LOG_TO_CONSOLE': EnvironmentVariable(
        name='LOG_TO_CONSOLE',
        filters=[validate_is_boolean_true],
        default_val=True,
        is_required=False
    ),
    'LOG_TO_FILE': EnvironmentVariable(
        name='LOG_TO_FILE',
        filters=[validate_is_boolean_true],
        default_val=False,
        is_required=False
    ),
    'LOG_FILE_PATH': EnvironmentVariable(
        name='LOG_FILE_PATH',
        default_val='logs/test_results.log',
        is_required=False
    ),

    # Loki config vars
    'LOKI_HOST': EnvironmentVariable(
        name='LOKI_HOST',
        is_required=False
    ),
    'LOKI_USERNAME': EnvironmentVariable(
        name='LOKI_USERNAME',
        default_val='',
        is_required=False
    ),
    'LOKI_PASSWORD': EnvironmentVariable(
        name='LOKI_PASSWORD',
        default_val='',
        is_required=False
    ),
    'LOKI_TAGS': EnvironmentVariable(
        name='LOKI_TAGS',
        default_val='application=query-validator',
        is_required=False
    )
})

settings.load_values()
