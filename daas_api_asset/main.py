# Get the current working directory (CWD) of the script
cwd = os.getcwd()
# Build the relative path to the sibling project
project_path = os.path.abspath(os.path.join(cwd, '..', 'config'))
# Add the project path to sys.path
sys.path.insert(0, project_path)

import sys
import os
import config_helper




if __name__ == "__main__":
    os.environ['ENV_FOR_DYNACONF'] = 'development'
    os.environ['DYNACONF_SECRET_KEY'] = 'AsDDm03I6mA6JCdhx16ozj5BDvMtYJMM54Qe2reDPgY='
    
    configs = config_helper.get_configs()
    asdf = config_helper.get_secret('DATABASE_PASSWORD')
    print(asdf)
