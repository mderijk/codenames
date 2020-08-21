
from .config import *
from .generators import GENERATORS

# all generator names and all generator names categorized by language, for convenience sake. (derived from SERVERS defined in ./config.py)
GENERATOR_NAMES = [generator_name for _, server_data in SERVERS.items() for generator_name in server_data['config']['generators'] if generator_name in AI_NAMES]
GENERATOR_NAMES_BY_LANGUAGE = {
	language: [generator_name for generator_name in GENERATOR_NAMES if '_{}_'.format(language) in generator_name]
	for language in LANGUAGES
}

# sockets indexed by generator name, so we can easily look up which socket to use to contact a particular hint generation model if we only have the name of that model. (derived from SERVERS defined in ./config.py)
GENERATOR_SOCKETS = {
	generator_name: server_data['socket']
	for name, server_data in SERVERS.items() for generator_name in server_data['config']['generators']
}
