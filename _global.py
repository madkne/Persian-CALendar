

VERSION = '0.94'
NAME = 'PersianCALendar'
START_DATE = '2019.7.16'
BUILD_PLATFORM = '2019@Debian/Linux'
PROGRAMMER = 'madkne'
DEBUG_MODE = False

# =>init global options
options = {
    'current': 'month',  # =>year|month|today (4 priority)
    'convert': '',  # =>english-convert (1 priority)
    'convdate': '',  # =>english-convert (1 priority)
    'setevent': '',  # =>set-event (2 priority)
    'eventtext': '',  # =>set-event (2 priority)
    'goto':'', #=>goto-date (3 priority)
    'lang': 'en',  # =>persian|english
    'event': 'false',  # =>events
    'info': 'false'  # =>info
}


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


"""
TODOs:
- pcal -t [-en|-fa] -i                      [DONE]
- pcal -t [-en|-fa]                         [DONE]
- pcal -m [-en|-fa]                         [DONE]
- pcal -y [-en|-fa]                         [DONE]
- pcal -ec 2019.5.8                         [DONE]
- pcal -go 1398.5.8 [-en|-fa]               [DONE]
- pcal -go 1398.5.8 [-en|-fa] -i            [DONE]
- pcal -bl 12d                              [....]
- pcal -bl 19m true
- pcal -bl 5y,23m,18d
- pcal -bl 23d,18m true
- pcal -go 1398.5.8 [-en|-fa] -i -e
- pcal -go 1398.5.8 [-en|-fa] -e
- pcal -m [-en|-fa] -e
- pcal -t [-en|-fa] -i -e
- pcal -t [-en|-fa] -e
- pcal -se 1398.7.22 "Hello World!"
"""