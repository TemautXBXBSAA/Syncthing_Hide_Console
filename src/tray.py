import threading

from pystray import MenuItem,Icon
from PIL import Image
from typing import Callable

from . import change_path
from .log import Logger,INFO

logger = Logger("pystray","log.log")
logger.setLevel(INFO)

class TrayApp:
    def __init__(self,icon:Image.Image,name = "TrayApp"):
        logger.info(f"{name} init")
        self.icon_img = icon
        self.running = False
        self.name = name

        # menu
        self.menu = []
        self.menu_name = []
        self.icon = None
        
        # thread
        self.running = False
        self.thread = None

        # callbacks
        self.on_exit = lambda x=1: x
    def start(self):
        self.running = True
        logger.info(f"{self.name} starting tray icon thread")
        self.thread = threading.Thread(target=self.__start__)
        self.thread.start()
        

    def add_exit(self,callback:Callable=lambda x=1:x):
        logger.info(f"{self.name} adding exit menu item")
        self.on_exit = callback
        self.add_menu("exit",self.exit)
    def __start__(self):
        logger.info(f"{self.name} creating Icon instance")
        self.icon = Icon(self.name,self.icon_img,title=self.name,menu=self.menu)
        logger.info(f"{self.name} running icon loop")
        self.icon.run()
    def exit(self):
        logger.info(f"{self.name} exiting")
        self.on_exit()
        if self.icon:
            self.icon.stop()
    def add_menu(self,menu_name:str,menu_func:Callable):
        logger.debug(f"{self.name} adding menu item: {menu_name}")
        self.menu.append(MenuItem(menu_name,menu_func))
        self.menu_name.append(menu_name)
    
    def add_menus(self,*menu_item):
        for item in menu_item:
            if isinstance(item,tuple):
                logger.debug(f"{self.name} adding menu item: {item[0]}")
                self.add_menu(*item)
                continue
            elif isinstance(item,MenuItem):
                logger.debug(f"{self.name} adding menu item: {item.text if hasattr(item, 'text') else item.__name__}")
                self.menu.append(item)
                self.menu_name.append(item.__name__)
    def __str__(self):
        return (f"<TrayApp: {self.menu_name}>")
