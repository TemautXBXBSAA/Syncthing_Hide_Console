# Notes:
# You may be wondering what this giant blob of binary data here is, you might
# even be worried that we're up to something nefarious (good for you for being
# paranoid!). This is a base85 encoding of a compressed PNG file, this PNG file was ONLY
# the icon of the app.
# You even could use: 
#   Image.frombuffer("RGBA",(128, 128),zlib.decompress(base64.b85decode(ICON))).save("icon.png")
# to get the icon.

import os
import json
import zlib
import time
import signal
import base64
import ctypes
import logging
import datetime
import threading
import subprocess

from ctypes import wintypes
from PIL import Image
from pystray import MenuItem,Menu,Icon

class SystemTrayApp:
    def __init__(self):
        logger.info("Init SystemTrayApp")
        self.icon_image = ICON
        self.icon = None
        self.running = True
        self.icon_thread = None
        self.hwnd = None
        self.on_exit = lambda: None
        self.click_show = lambda: None
        self.click_hide = lambda: None
    def create_menu(self):
        logger.info("Start")
        return Menu(MenuItem('Show', self.show),
                    MenuItem('Hide', self.hide),
                    MenuItem('Exit', self.quit),)
    
    def show(self):
        logger.info("Show click")
        self.click_show()

    def hide(self):
        logger.info("Hide click")
        self.click_hide()
    def quit(self):
        self.on_exit()
        self.running = False
        logger.warning("Exit")
        self.icon.stop()
    
    def run_icon(self):
        logger.info("Setup icon.")
        self.icon = Icon("app_tray",self.icon_image,menu=self.create_menu())
        self.icon.run()
    
    def start(self):
        self.icon_thread = threading.Thread(target=self.run_icon)
        self.icon_thread.daemon = True
        self.icon_thread.start()
        logger.info(f"Start icon thread: {self.icon_thread}")
        return True

def hide_window(hwnd):
    try:
        logger.info(f"Hide {hwnd}")
        user32.ShowWindow(hwnd, SW_HIDE)
        return True
    except Exception as e:
        logger.error(e)
        raise e

def show_window(hwnd):
    try:
        logger.info(f"Show {hwnd}")
        user32.ShowWindow(hwnd, SW_SHOW)
        return True
    except Exception as e:
        logger.error(e)
        raise e

def enum_hwnd():
    windows = []
    def callback(hwnd, lParam):
        windows.append(hwnd)
        return True
    result = ctypes.windll.user32.EnumWindows(
        ctypes.WINFUNCTYPE(wintypes.BOOL, wintypes.HWND, wintypes.LPARAM)(callback),
        0)
    if result:
        return windows
    else:
        return []

def hwnd_get_name(hwnd):
    length = ctypes.windll.user32.GetWindowTextLengthW(hwnd) + 1
    buffer = ctypes.create_unicode_buffer(length)
    ctypes.windll.user32.GetWindowTextW(hwnd, buffer, length)
    return buffer.value

def run_process(file_name:str):
    try:
        return subprocess.Popen([file_name], creationflags=subprocess.CREATE_NEW_CONSOLE)
    except Exception as e:
        logger.error(e)
        raise e
def hwnd_get_pid(hwnd:int):
    pid = ctypes.c_int(0)
    user32.GetWindowThreadProcessId(hwnd,ctypes.byref(pid))
    return pid.value

def main():
    process = run_process(EXE_FILE_NAME)
    logger.info(f"Start {EXE_FILE_NAME}")
    logger.info(f"Part of title: {PART_OF_TITLE}")

    start_time = time.time()

    while True:
        logger.info("Trying to find process...")
        hwnd_list = enum_hwnd()
        process_dict = {}

        for hwnd in hwnd_list:
            name = hwnd_get_name(hwnd)
            if PART_OF_TITLE in name:
                process_dict[name] = hwnd
        if len(process_dict) != 0:
            break
        if time.time() - start_time > 20:
            logger.error("Process not found.")
            raise Exception("Process not found.")
        time.sleep(0.5)

    logger.warning(f"These Process will be HIDDEN:\n    {process_dict}")

    _ = 0
    def hide_all():
        for name,hwnd in process_dict.items():
            if hide_window(hwnd):
                logger.info(f"Hidden: {name}")
            else:
                logger.warning(f"Failed to hide: {name}")
    def show_all(): #By doing this, the process will be visible if they're still alive
        for name,hwnd in process_dict.items():
            logger.info(f"Show: {name}")
            show_window(hwnd)
    def on_exit():
        for name,hwnd in process_dict.items():
            logger.info(f"Show: {name}")
            show_window(hwnd)
            try:
                os.kill(hwnd_get_pid(hwnd),signal.SIGTERM)
                try:
                    process.wait(timeout=2)
                except subprocess.TimeoutExpired:
                    logger.warning(f"Unable to wait for process to exit: {name}.")
                    process.kill()
                except Exception as e:
                    logger.error(e)
            except Exception as e:
                logger.error(e)
                process.kill()
            try:
                os.system(f"taskkill /F /PID {hwnd_get_pid(hwnd)}")
            except Exception as e:
                logger.error(e)

    hide_all()
    app = SystemTrayApp()
    app.start()
    app.on_exit = on_exit
    app.click_show = show_all
    app.click_hide = hide_all

    try:
        while app.running:
            time.sleep(1)
    except KeyboardInterrupt:
        logger.warning("Keyboard Exit")
        app.quit()
    

### Init Constant
SW_HIDE = 0
SW_SHOW = 5
EXE_FILE_NAME = r".\syncthing.exe"
PART_OF_TITLE = "" #if not given, use "os.path.basename(EXE_FILE_NAME)"

### Logger
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
ch = logging.StreamHandler()
ch.setFormatter(formatter)
logger.addHandler(ch)
fh = logging.FileHandler("latest_log.log", mode='w', encoding='utf-8')
fh.setFormatter(formatter)
logger.addHandler(fh)

### Save&load config
if os.path.exists("config.json"):
    logger.info("Loading 'config.json'")
    CONFIG = json.load(open("config.json",encoding="utf-8"))
    EXE_FILE_NAME = CONFIG.get("EXE_FILE_NAME", EXE_FILE_NAME)
    PART_OF_TITLE = CONFIG.get("PART_OF_TITLE", PART_OF_TITLE)
    logger.info(f"EXE_FILE_NAME: {EXE_FILE_NAME}")
else:
    logger.info("Creating 'config.json'")
    CONFIG = {
        "EXE_FILE_NAME": EXE_FILE_NAME,
        "PART_OF_TITLE": PART_OF_TITLE
    }
    json.dump(CONFIG, open("config.json", "w",encoding="utf-8"),indent=4)

### Other
PART_OF_TITLE = os.path.basename(EXE_FILE_NAME) if not PART_OF_TITLE else PART_OF_TITLE
user32 = ctypes.windll.user32
logger.info(f"PART_OF_TITLE: {PART_OF_TITLE}")

### Icon
ICON = '''
c%1E>iCa@=_Q&T>V5a@e(hU%`YDdNHwoXg8nNC-&wbrQ%S`@d^*s85sZPZ$KQM)LLfTFBI*uuW4fVe=
EJ&77+6}PxlZ0ii?_ns>^-X!<l+%4R&oagyGB=^4WdCz;k=f3w%faDK<=v_8A)9ghEAZQ3$LQxl10*H
X_7uw}#EWuyx`SqK<4b~H_^+X@NSx2yl)L0sNQWtts7kW|?db5|>Ip|9^NN@Hb1QK)vE6G2o4T-}*&=
UIB2RGOty~&F}G&f<M!Lu=02%&`jT99djGE4!4NCNaw41_>J|2;y4b>+<B0s1M0l@LnsQ9HMuY6H_vU
IZ<nH|g#KnO`KqN9}xjl97A_qV5FfLtq{B>H7kie?TA9or#s8Ra=Mdwt;D6txq%Q2+$9Og%F^&F5O`R
(~KH|)dO<wffyqRz4D&mmumDP=={=*&<_u(MhhW8ZM~E<oDacDfPMs{Ra-YD%rC{LRU?1z6rG2~m2I%
C;R@uo-GcHf9ngIHcW`Ale*YiU7Qw!&t1rQSN}6Dl-rW5)kYX$%^vL@G#!b)>pgTZ~P_OdK9WFJNYIW
Ctg`^8NsJf!+p?l_LCG@EGk_Qm&2?heVli*`5aFFPM*Q^?b^?>WcOS$LVI!}U?5U94ULTrG}=ufZ`z#
Y6@cwSY_xh%K!7A&f0bIY6=1gfnspAFD85bYa?_6?vkla4f!wf(l*GP|@Uvd7p~e+B$AOp52A3ys=3v
)O=TqJ6UR+N17G0`_g5X1G4NtqzhKBGuNLX}&~zU(`OCicJwF9ai>wM_)+9nQO3>=)wiA<JeBA`wRM6
bh1scywH$*Yt_~rjn>}xUQDtXnQo#qlB+dpIqPUM{3H9Utaz{vSDkLB>OxLU)RMg-`cf)ST?DGCeNux
L!AbxnK)s~o82cPNf1T<-GR>q&EL^;uZ-K3KS0vw)BFxv6j!~5w=+fSx#2hdmsGnHNZMj8h?oPd3)dK
1%wq|iHz`hE`((UgL_#CX)DG~cyBoCMmF_uVbWlYu?)pU1c1gYPJCt5|V30N}=Pqr#DKGDKT@aabFwF
HpMtTJ)yJ*9i*8QJ5y6R~xGb5dw*1HtX@6_YUnl**G(J9_E1$Lr2yM5>AG5iSd^ZJZzWQDAJhzAp4ht
oI^V2_T0=f%kgM->lMRS!1aQ)+}l(#A>a-!iW@;65|HCQGZ=`X`e&(b_(S~byl5f7qk{AR0DW@`Y5fv
cS60!oA{SQqD7eYUmkCjHI66p?_3L|uaFuTPHI5bcnS4I3Ty90uo6HjdrYq1)4^*5^CV{+PiDBz1Ub#
Ogw+6PD|0->eox??P^Xg<3trEz=X{6E*{Hfk-GPvG5Nkl*ICbQDt&{zFz&pM!fB;gNSae>P_Q^)cWAs
G6Jl5heFIXos$C3Sd;Ia5R3jw6?LWY^F>Hl@9{ojf9Qpf1Yd?BC)w1$gv#|e<EeOz6joUu{ce(mMgK+
`Yx-%rBVlY5L;;iJOy!p4ZJle`xseJuo#0><c4`y`_z-@Of2x#F^;?YH60>~liK5WNPFJ{qa>!P?|Ay
eGVnZdN_-o<!m~@xT9~4c8DC{zb0=kH(T~KbG_r30~98^@`1?nw8+YH-mYTV_%fF@cJiu3SI*qjjatN
fE2b=U*e5ZTiGVbZ*M1D;yr*iTvJD<nfS&KyatfA7AbSU@%aqzS8C_k6LFO{p(Y@|F8@y8(U{r*0!Sg
@oRzyie<SsoYLeu)w-eqV@7iaYiyXUrKLFcEnZty9{ym?zqD}QYdn&H>OJdAbo*y|-%lV!lo+E%1%G$
Yq&slTrjwGLbfnkXaifNCQ-E`B{n1MX{2TGa4^C|rIFI*ec&a<cDYTXoTcpbVJ)4-|!{#pY8#FB89`@
Uax@wRAxeTfNq3hOT{-#*UT*Z2@XEW;A&dE=RoXA$kQFX1YGVvSn=U61SZyWxlT*8~zkEZ?4N<Eh18M
EmQDD7pXJeEO1*F`e!K4@cMN2p|^R+i}^4xfap>`XYQe6l?#?I3sjiF9-dtV&lfKxD0Dr?Yw$AL*wfq
yYZ%C+EeST@bSmmwBJ_~Kmf7eTEk`Eo@f*8uP^a@vQg3N9*w&8g~t#|>;KTc8Z80D!WaK@WPVb7_66Q
ZKSRAAs-$U3o5jXqVCb(CJBJ~0-1}Cn3$=6Xsi00u+wQt6(&E`$P3-~5PYVIWFr)ASXFMy8w~F%BS3s
SFSj|;&_l2y+8&YEmz#33`E^nlpRnN62F(kH*(nyF=*D~qzT#}Kxj&M)s%J5zyF*fZ(QKSZ<$YYU|wX
w%V#UjC9Z{@jzM#0y!rlgtI7w<KfW|k6P<lmyIH3Sd~mt|eJA=+1O<#nQokbNGu!M3jaP3O7i;yDR17
7?^k=EY^34DG7t-4pn{MA$wL*M?`w8X?3dwo^Fo*1tuP8i*v1MKC_=9CsZSToC1}H?pf%*gg-}%Eu4X
iSo_oOJcmD^~YM{ve#41s^?!VP)pQ7h+&OL8KabA--XAe`1@-_m6ZTu;L~5MuinBl2@Qhxd7mF{k~|J
yeRbDdxoQyiF>33e2Ct=<1n={(t(>tu;o9R{gVfeSNj}ItOXZtpd3mdoet0blF<cvPjgTADrb>nN-y<
Gg{U!MGBnC&<!mgUjyw`K%t=}l!v7HdhI)8)mt3-T!^@jB-*56+wz^A_yf1W~M{&~fJFM~CrWQ^m8#$
1NyMEeXEPiZTM{^Yn6f1W_dAz|yd7(<^*$2m^Vqdz$(-sfr2@ar$$pW3{pQ|A9~XruOd#HTxAb*;Zhp
S#7wrGL$p4j8<zMv_l8!TY&VhB<gTuHJ32j?3WDpPUox@6Qt8(w~`wkVB1<e0Mh(r&5+l_IZQ$)~FWm
Sfal>$Huwg9EBRz$y2fQs%y-LnEAM}Z;rOOJ>HEK7dgk5<a3uW21V6C^%e2ot#zH;3tvq#2_8pDu=d8
LpQZSwtcA)Qf^~^VnGc_3T5h;~PQ3cNaa=jM!WzK(Q6diXLu>k3aidLB%ss8ET83l0TYsD<n_-S6`3y
T<L;yZEoaC-KQMut6gVuCfjs-T7@sK#<HJhf_6@Fdr4l8ZF#XCnOz%i5@`~SjD6%l}ofsxgU<vy(H5(
UPJG~QHh-|Y#8bK=XT5^!0j<+@a#p?v2*D^hNM+}kbIc-5`izryqPAGk(K^1JhtmH=F23jECGego=S;
mf65_^!pN*%m224TQ0LZAx2Qe_nA<GraHMypULhK6?f4kpm;D-KsxdtWO@Olj2kN;LcP21mL2ihv<*_
$5>0cG~ICGBE|cuXD9*^jc%PIj>VTpCE(gG;oK$q)Z+htJh+2A=0I)zX-)AyL~A;QtaY@me6b4!YeVi
HchvqmMPlIs{c{=SMxx)bUHTVwr~dd}0<9~p>HNY*o2Gtb9d&0e*}$5TQv)~`cgDA@l>2jn@tj1z)aQ
Ua__HCD0BkH1_;<`gEc4uT)-gPVfP@BFuSqwYXmeX^)t9;7e;XBDE5)ak{{K(%cq~^t^sSW5FSww(#;
zE!rwY~+9i`R*){xRM@o9i{A<?gn*8hQ@4PFG`BDP-s9vSn=H-;zja(n|!$vg+^kGE00mtv-#^BL-)b
R0W*K4)PmS)V2PwfhX92Yxab2*AdG@G7|etGxXY=8nsMPXlX#&rmNV$K%WWsC~6k{rWiQujOlx*Mig<
z;$13&6LK~zF4Vx$J}ul#vswJ#qsl>9{ADVPXIn%j%$DmBJYcMt+?{r6Y<|$%X>ZG{myrHmF#i&_964
~FG%$p>Zm{3pMEr02*3x<2{jeE7L+vK;`P^)S$c&3wUM5@-jU-U_2n|mzYO23p9B7<A1gx%Ae71av#|
bH8wH=en`{#7v!|gy%m4ck%#jqozPnEIuC<tRi7`8^{Wkr7sPrd*6k>Q@Bj7xw`t@{BC%&~1&tV&}e)
+B`sXn`4UHcg|V36Y1e{T)%bwJgt2k7MvCiDDFHX3yg^qgG!@ag}@?UjK9kU~ry_ZomTJ2I+9l3$t!w
^hI+TTjBk(BtsLmU4J<^HCVRsT2Y>mcZ*9kHEh+9ENw+AA)h~i($gLBAB$c2&S$rq?rDF0R(-YZzGs6
cTJv+V8%HF+tYo~5BfvD=pV<y@o-!mALH1Na|SFe*Wv2*JMbIJcOEV|+$4COB|P5|i+S`3J1sSbF24h
YwDBTXrTE9V_}0Rz%N?A3|4g*?2|YpS`t+tUczMGS`1iU)@FB_llr;q~^SeBly*jtY5VEcSmi=%9Hbo
tWh?HuG&ojdNJMYa8=ZW)W%fk{E|4%wM@4TFADA1MuR1Iva3?+aRmhk)^RcB`>Y%6Vsp_|L$xecZ8`n
tm~?)xH`wwhdzt8)7sbJrKb{Ou+1(Y7)wA8&;l;Ig%Y$`kALbE!j;CS7pu`&jh%kueSx=YRj#2~8JoL
W!XnVlwMsUBoe%N7mJuD|7mB0p<zwg?YpLHMZTP^7&Fsy&V0uLiI=U+Ex)s0HHiY*0kXp%OGIwA(%|=
nYac9eVg5nLSS8tC+j5U7xRqy7NL)oAnLooy|z~P5P*xnY&iiV)|bMoYl`4wZ7$4Mk=0K(gL%jNqYkJ
Ck6xm#eMSvLGX3~&Du?IS9)__i^B{0}CQKJeUa9@-q&vUfg^;y*g8Q9ox+Z!|caU1pK*b~^c0RU8AE$
`bSIdqG^*~)vAJmDVo0TBy+NbT0p%q>OHyphcu$o-s%d=qGGQBKvOPs$ipw`?jxF6~-HwL+E+jq<sJH
{o)7t@rE6ZJyfd^eVVE=7CVUR#-8JY{JHC;^-PXuA_C1ob=DcukQw<dTwKPsKEEO^z%-Omjz^<CbT4$
kCp*@yjyre)4rX$R+0p`{#z@ePGV&Y?uAcHeQt-gCnbV9HIOp2hyr+$MG>9`)YHc?U*jF4nm{Ko!ZmS
YfbIcJn%8bdZN17ZeG|I+u*rf@fCJCP<md-i>nHqzUN7bjn)=uCM`|{xnv*a{+x{((?ys4FmFo4!DP|
Ke7icNkK<!B92=j9#hri?Rn2yDpwBT4W4w0b{@?0hAIEW8+iz0yWt!6SdSiLESqbfFd+nQS^Tb6dAO}
AE(RPv?^Yz2r^7+U9*cRK-V4m@q_NQXbey!~{>|(&S_qDn~wK-nZWb@C|AI~u@I`tH6iYT+I2gkW%n_
1dSyMA(W%VhlGw9cnj7J4hG|I^w6@Anp`-TmlG9Y`hX5dU}F-}&`-n7KmF+3)OytE_%^#2$xh*X{p47
N4U(reS~W55-RXlXC9=zUBDoCcEco7!&$)oC7|_V@$*6oA#92jfuzbCvAA1t)EhiUXiy}N$qKSc6pxW
!v)D86<7MBRU0pI_B(UoiqpA$I)jrB)C$inSexT?4r^k?_98nU%yxJlV_?<})&$}>2Yigjn1;_chL_l
$(=p>u+VDJEKP7l&Nv5LfzN5XkG^_XnO%g~Uv-rM_%zQZ7PX~^1_G2E`tj%Wae=w`s)~4F%{Cjk)569
S;?NEF4!4?x83mQJgV@$*68+P04kH?tv#q(_a<npgYX&s|h<SV-Fv)OA4)2w4d4uV+pMfbkz`po$&5V
9uQX?<qqKX7RpYd@yHW2e~vA9mfYBTjuCEh?$f&KEwXt*W67zS&w}7Z001e2mAKhR<<)oBmxfGyCCKI
6udJa(G9R-1+3P+==ei9&O~ZJny$ck~-g;p9o@L>d1V~W~c#IKbnp^?Dg~6cUiVJkq0YS+c5njQ@_5y
k59;~qK;j=e(yW&%SoL%#zO0l$C!rC*M=Ro(;tsvOmw{Xv*qFqr+#vH=IiY6?$Dk#|0UTI-~24G^PPF
|Ae4;4d*2ynK7ZMEtmPv2-_OPCPjmL0w_4BHk2&V|I}fq8L2Vu5i#T|a8Vh|hpD)>xXXg)(A^4b%kA{
woevUqvG2@)*F&z6zW%Q!-%I?&jwx<^B!{3?{2SUjxth4DzANzV!E~k!ooy=XC!P;-lj$+P!%rS+w>#
2<XBF(M)Jy$krkv{y*;8+ksdO??tmdmWi*$msV_51GUBF;Wc-$L8<L|*<ZNs;$=<=Ut(({=xx6$7qFW
9aC3uDOl-K5*4~+o|8`pSX2p`W4!)r}2;Z2RoklD%<UQeWCVDh|c_a&;j5hE&tyCv6?KGoX#y=&;DAD
Y0Q4JmZx#HWBOh7V<Bfvxr!J2A{d*iwyyYSL88r{TwgEFP3#!DILl+Sr_EoJTKwv#`+<v8hW>o#`SfS
D=i2`VEl;(z*%fz;wauxz7S1@a5Bf&(N=&wT`Ep$rY>Bx4+78z&x(~g6VPAZXG2pQeHHlDGVX^t5AEO
_>TygQjoP>@ci#$(z+J<Y=!e5yl4Q!<5-FsivbnX)Cd8E0`%B{acKg=bYt=wMVG^V5Niao|UKK7*z`{
FSi7Y%hAACh2KcR|ZisAIHYOxPzT)j&aykMp9(z&gNs;>rORql4o+9$%R0vD(x2geEoo<-mR5ND4!Lw
)4n>@9lpt;;28f?Tn>5)^-O{D{XB~)jI!=9_F5F{8C0uX}9Ow#f=sgTW;3|$J!iz|MfoB2KH$pdSiTa
?a<?5e>{$G#lXg>c}c47^Tpbb1?dxC42<r4Y3g2}Ny)9Y>Bv0p2;GiNf5*0AG36}!{z9Fbu_W2)9O|=
Rjh=ICre5D}&2x$eA8*=y|2>7KRx9KkvH!gWp2y>S@nIXj955L<FIkn>_i}B}f{Zaw2gP=bnGyvEok!
!jcA$@Of%$VZu6`RyE-|N$Id<G1V1Lbb8NB0S8`@S7{h4vo`r|R?co?gJvCiPR{V5f|oHyHEh4#<I=)
irQLqk%!^?g01ZQz0o?-8>T%`Z-lgcYH=pv$R-od?PQpY!qgcj;7HCa(Hz+*M4qLk($A7d(dkT#bq39
=`wnF8UL44E4t2Obh%f$<_|zet&KZ6$i5p@Htl;PkkEGF<6t<E$`=dhdn-D7yj(jy`7^!i2zS#>Q@JC
8s!k}@EE-o;ZM3<$m(>Pj@a(qIS1_41G=4|wh4@9+ilM`FzRFnsSCCk{vMoQ_S2+${60^t`Gus7895`
y`uwCl;K_unN&`bplTAykhmsR#;how0?b=<rcJCgrA*_gcjyj`7C!e(Qg+B0{F1yNBOF4(?oyL7;a#Z
Kw`8v1!?S?1W;5kXUr#^}5eD>o#&{vqeFcFq*&Y^fac)!#6VKd{+z9GHun&&c~kTmb1L2>41CWb>_X2
jI!4!?OiMgC5=Cz|hEo#u&Y`>jt+*bRM&Q6EQi`UNNT=)Jv?<~t`@Gi++K^~n!+L2t%?;-1byK?%j)^
HclGS}(?YW+!WgPKmaT8XpF|iQykd+#MJcU;Nm-lz!a>*kiMkCk_fcU>^CwPUy)zK6#(jXJ%smIxo>4
nXB{mnVAqiWKv|uh;cihCopVc_+7v0F_n+bNgkti{(6%=5}Z87XGXm4@rjWg!{6Tlp2W}z;dcj2Bbv`
j>NW4#d9pn`JK6iupoFzPQx8-Q{wSj3iT8en?quk=uui{E_O*IXkJCLIoYa4vt85PiCwo5}l&JBZ7E|
myIoj;^ain#~*qxoj-u(&WGHAk{jsgGK+lsy)`7~keL$i91-v19}YL&t'''.replace("\n", "")
ICON = Image.frombuffer(
    "RGBA",
    (128, 128),
    zlib.decompress(
        base64.b85decode(ICON))
    )

try:
    main()
except Exception as e:
    logger.error(e)
    with open("error.log", "a", encoding="utf-8") as f:
        f.write(f"{datetime.datetime.now()} {e}\n")