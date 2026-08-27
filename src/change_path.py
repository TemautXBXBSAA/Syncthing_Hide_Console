import sys
import os
from . import log

logger = log.Logger("Change Path","log.log")
if getattr(sys, 'frozen', False):
    logger.info("Running in a PyInstaller bundle.")
    application_path = os.path.dirname(sys.executable)
    os.chdir(application_path)
else:
    logger.info("Running in a normal Python environment.")
    os.chdir(os.getcwd())

logger.warning(f"Now working in {os.getcwd()}")