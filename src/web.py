import webbrowser
from .log import Logger

logger = Logger("webbrowser","log.log")
def open_web(web_url:str):
        logger.info("Open web click")
        try:
            webbrowser.open(web_url)
        except Exception as e:
            logger.error(f"Failed to open web: {e}")