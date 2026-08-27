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

ICON ="""64,64 c-rlo(GA2f2t&I|_n+}P!Kp1^Y*QlL-$~(_grotE13S+1{AGTJ
;m9&OYJp-_*P@$SNe4DNO9K^dh7PLi9U4S!iVhVGI+-iAV6dY{
w+2<*)jD?YSJ;}3XDkgewxMEsW<GcJP7NY9bf5DP8>X<MG>FW}
zVAiiW0mh!?!0d`_zL?Q4VK@Jy^8<M9BSXYnQsPn-+!6E;+xTR
?RUJPsQUhnwNe8&_G;Um@41usBl~*_e>ApD;LpT$cmC{|=ERRU
%U$?U_n1liEZdPbq3^IAwsz&cRQbC`H~%DdHa|PgJjn-S`I-5Q
jPL)w|1j85dpE+5JeScLL~~&i_#?i*djnO;b65Z0A^#J7?}+As
)iijz|EhA}N^io*`-VgP1B&0F287A3Q2)eO_evVD+1d4vtaYza
|60jEt^T>w_e%Be4BxZ+A5^%v|7H81w*PJWAGiN?`=6)vzh8H;
_!|"""
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
