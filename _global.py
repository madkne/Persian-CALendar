

VERSION = '1.23'
VERSION1_DATE='2019.7.19'
NAME = 'PersianCALendar'
START_DATE = '2019.7.16'
BUILD_PLATFORMS = ['2019@Debian/Linux']
PROGRAMMER = 'madkne'
DEBUG_MODE = False
#----------------------------------------------
# =>init global options
options = {
    'current': 'month',  # =>year|month|today (5 priority)
    'convert': '',  # =>english-convert (1 priority)
    'convdate': '',  # =>english-convert (1 priority)
    'setevent': '',  # =>set-event (2 priority)
    'eventtext': '',  # =>set-event (2 priority)
    'goto':'', #=>goto-date (3 priority)
    'addsubtract':'', #=>before-later (4 priority)
    'issubtract':'false', #=>before-later (4 priority)

    'lang': 'en',  # =>persian|english
    'event': 'false',  # =>events
    'info': 'false'  # =>info
}
#----------------------------------------------
class TerminalColors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'
    YELLOWBOLD = '\033[1;33;40m'
    REDBOLD = '\033[1;31;40m'
    BRIGHT = '\033[1;37;40m'
    NORMAL = '\033[0m'
    GREENBOLD = '\033[1;32;40m'
    GRAYBOLD = '\033[1;30;40m'
    ITALIC = '\033[3;37;40m'
    BLACKWHITE = '\033[0;30;47m'
    CYANBOLD = '\033[1;36;40m'
    WHITEBLUE = '\033[0;37;44m'
#----------------------------------------------
PERSONAL_EVENT_COLOR=TerminalColors.YELLOWBOLD
HOLIDAY_EVENT_COLOR=TerminalColors.REDBOLD
OCCASION_EVENT_COLOR=TerminalColors.GREENBOLD
#----------------------------------------------
"""
TODOs:
- pcal -t [-en|-fa] -i                      [DONE]
- pcal -t [-en|-fa]                         [DONE]
- pcal -m [-en|-fa]                         [DONE]
- pcal -y [-en|-fa]                         [DONE]
- pcal -ec 2019.5.8                         [DONE]
- pcal -go 1398.5.8 [-en|-fa]               [DONE]
- pcal -go 1398.5.8 [-en|-fa] -i            [DONE]
- pcal -as 12d                              [DONE]
- pcal -as 19m true                         [DONE]
- pcal -as 5y,23m,18d                       [DONE]
- pcal -as 23d,18m true                     [DONE]
- pcal -t [-en|-fa] -e                      [DONE]
- pcal -m [-en|-fa] -e                      [DONE]
- pcal -t [-en|-fa] -i -e                   [DONE]
- pcal -go 1398.5.8 [-en|-fa] -i -e         [DONE]         
- pcal -go 1398.5.8 [-en|-fa] -e            [DONE]
- pcal -se 1398.7.22 "Hello World!"         [....]
"""
