import _global as Glob
import display
#=============================================
def PCAL_BasicHelp():
    print("{} - PCAL - Version {}".format(Glob.NAME,Glob.VERSION))
    print("Usage : pcal [options] OR pcal [argv]")
    #=>arguments
    print("Argv:")
    display.PCAL_DisplayTable('Arguments',
    ['-v | --version',
    '-h | --help'],
    ['display Version information',
    'display Basic help'],14,hassplitline=False,usingcolors=False)
    print("Options:")
    #=>extensions
    display.PCAL_DisplayTable('Extensions',
    ['-en| --english',
    '-fa| --persian',
    '-e | --events',
    '-i | --info'],
    ['display english numbers and names (by default)',
    'display persian numbers and names',
    'display events of day(s)',
    'display extra info like weekday,interval,long date format,is leap year,english date format'],14)
    print('\n')
    #=>main options
    display.PCAL_DisplayTable('Main Options',
    ['-y | --year',
    '-ec| --english-convert [date]',
    '-go| --goto-date [date]',
    '-bl| --before-later [count] [before|later]',
    '-se| --set-event [date] [text]',
    '-t | --today',
    '-m | --month'],
    ['display a calendar for the current year (ext: -fa, -en)',
    'convert a english format date like \'1999.4.7\' to persian format date like \'1378.1.18\' (no ext)',
    'get a persian format date like \'1398.6.14\' and display a month calendar of that date (ext: -fa, -en, -i, -e)',
    "get a count like '5d' or '18m' or '3y' or even '2y,10m,7d' and get a parameter 'later' or 'before' for add or subtract (no ext)",
    "set event as a text for a persian date like '1398.4.11' (no ext)",
    'display today date and persian-english format date (ext:-fa, -en, -e, -i)',
    'display a calendar for the current month(ext: -fa, -en, -e) (by default)'],42)
#=============================================
def PCAL_Version():
        print("{}(PCAL) {} ({})\nWritten by {}".format(Glob.NAME,Glob.VERSION,Glob.BUILD_PLATFORM,Glob.PROGRAMMER))   
