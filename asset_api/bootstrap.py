# bootstrap.py
import sys
import os
from dotenv import load_dotenv

def bootstrap():
    try:
        # Load environment variables from .env file
        load_dotenv()

        # Set up the project path and update sys.path
        cwd = os.getcwd()
        project_path = os.path.abspath(os.path.join(cwd, '../..'))
        sys.path.insert(0, project_path)

        from daas_py_common import model
        from daas_py_common.logging_config import logger
        from daas_py_config import config

        # You can call other initialization code here if necessary
        logger.info("Bootstrap complete")

        # return logger, config.get_configs()
        return logger, config
    except Exception as e:
        print(f"Error during bootstrap: {e}")
        return None, None