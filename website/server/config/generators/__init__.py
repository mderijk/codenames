
import glob
import importlib
import os
import sys

# assemble all GENERATORS dictionaries from all modules into one global GENERATORS dictionary
GENERATORS = {}
script_dir = os.path.dirname(__file__)
for module_filename in os.listdir(script_dir):
	module_path = os.path.join(script_dir, module_filename)
	if os.path.isfile(module_path) and module_filename.endswith('.py') and not module_filename.endswith('__init__.py'):
		module_name = '.' + module_filename[:-3]
		module = importlib.import_module(module_name, __loader__.name)
		GENERATORS.update(module.GENERATORS)

# https://stackoverflow.com/a/1057534
