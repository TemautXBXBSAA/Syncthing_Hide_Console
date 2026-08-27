# -*- coding: utf-8 -*-
# Platform: Windows only
# Notes:
# You may be wondering what this giant blob of binary data here is, you might
# even be worried that we're up to something nefarious (good for you for being
# paranoid!). This is a base85 encoding of a compressed PNG file, this PNG file was ONLY
# the icon of the app.
# You even could use: 
#   decode_icon(ICON).save("icon.png")
# to get the icon.

from src.log import Logger
from src.icon import decode_icon
from src.config import *
from hide_windows import HideApp

DEFAULT_CONFIG = {"EXE_FILE_NAME": "syncthing.exe",}

ICON = """32,32 c-qaE(GkEP2t&Jz`_D)xP!f`O_RhZ^4=@N+)mOk-YZY?}wCm=&
{7|`yAB~;kr}{AEqJFS!(l+$(lug_<?Ze52pt-G$G#kl9$2Zm8
)`xWLtbT9Aj@D0#jqp>NyTNbt9_4p=PVkvKX5Vjj4^-_MdS9EH
G<(8V`V6D32^(Q_ebDs=vUTt7zpOT#Gl0T&%wMd2-Sejsdt&~c
upRq{%6?)0dSU;(wSWJBg=!="""
logger = Logger(__name__,"log.log")
def main():
    logger.clean_log()
    logger.info("Starting...")
    config = read_config(DEFAULT_CONFIG)
    app = HideApp(
        decode_icon(ICON),
        config.get("EXE_FILE_NAME","syncthing.exe"),
        "Syncthing_NoConsole")
    app.start()
    app.wait()  

if __name__ == "__main__":
    main()
