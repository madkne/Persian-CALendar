
from sys import argv
import os
import datetime
# import jdatetime
# ------------------------
import _global as Glob
import help
import display
import convert
import common
# =============================================
# =>main Persian-CALendar interpreter


class PCAL():

    # =============================================
    def __init__(self):
        # =>if has any parameter
        if len(argv) > 1:
            # =>if argv is -v or --version
            if argv[1] == '-v' or argv[1] == '--version':
                help.PCAL_Version()
                exit(0)
            # =>if argv is -h or --help
            elif argv[1] == '-h' or argv[1] == '--help':
                help.PCAL_BasicHelp()
                exit(0)
            # =>if has options
            else:
                self.OptionsAnalyze()
        # =>analyze options....
        # =>run convert function,if exist its option
        if Glob.options['convert'] != '':
            self.convert()
        # =>run set event function,if exist its option
        elif Glob.options['setevent'] != '':
            self.SetEvent()
        # =>run set event function,if exist its option
        elif Glob.options['goto'] != '':
            self.GotoDate()
        # =>else run display current month/yaer/day
        else:
            self.current()
    # =============================================

    def OptionsAnalyze(self):
        largv = len(argv)
        i = 1
        while i < largv:
            # =>main options
            if (argv[i] == '--year' or argv[i] == '-y'):
                Glob.options.update({'current': 'year'})
            elif (argv[i] == '--month' or argv[i] == '-m'):
                Glob.options.update({'current': 'month'})
            elif (argv[i] == '--today' or argv[i] == '-t'):
                Glob.options.update({'current': 'day'})

            elif (argv[i] == '--english-convert' or argv[i] == '-ec') and i+1 < largv:
                date = argv[i+1].strip()
                Glob.options.update({'convert': 'en', 'convdate': date})
                i += 2
                continue
            elif (argv[i] == '--goto-date' or argv[i] == '-go') and i+1 < largv:
                date = argv[i+1].strip()
                Glob.options.update({'goto': date})
                i += 2
                continue
            elif (argv[i] == '--set-event' or argv[i] == '-se') and i+2 < largv:
                date = argv[i+1].strip()
                text = argv[i+2].strip()
                Glob.options.update({'setevent': date, 'eventtext': text})
                i += 3
                continue
            elif (argv[i] == '--before-later' or argv[i] == '-bl') and i+2 < largv:
                count = argv[i+1].strip()
                typed = argv[i+2].strip()
                Glob.options.update({'setevent': date, 'eventtext': text})
                i += 3
                continue
            # =>extensions
            elif (argv[i] == '--persian' or argv[i] == '-fa'):
                Glob.options.update({'lang': 'fa'})
            elif (argv[i] == '--english' or argv[i] == '-en'):
                Glob.options.update({'lang': 'en'})
            elif (argv[i] == '--events' or argv[i] == '-e'):
                Glob.options.update({'event': 'true'})
            elif (argv[i] == '--info' or argv[i] == '-i'):
                Glob.options.update({'info': 'true'})
            else:
                display.PCAL_RaiseError('bad command : '+argv[i])
            i += 1
    # =============================================

    def convert(self):
        """
        english date limits:
        year: 1900...
        month: 1..12
        day: 1..31
        """
        # =>init vars
        cyear = 0
        cmonth = 0
        cday = 0
        # =>debug mode
        if Glob.DEBUG_MODE:
            print('convert')
        # =>split date
        date = Glob.options['convdate'].split('.')
        cyear = int(date[0])
        cmonth = int(date[1])
        cday = int(date[2])
        # =>if convert mode is en=>fa
        if Glob.options['convert'] == 'en':
            # =>check for basic validation english date
            if len(date) != 3 or cyear < 1900 or cmonth < 1 or cmonth > 12 or cday < 1 or cday > 31:
                display.PCAL_RaiseError(
                    'bad english date format : '+Glob.options['convdate'])
            # =>convert to persian(jalali) date and then print it!
            else:
                jalalidate = convert.GregorianToJalali(cyear, cmonth, cday)
                pdate = jalalidate.getJalaliList()
                print("{}/{}/{}".format(pdate['y'],
                                        pdate['m'],
                                        pdate['d']))

    # =============================================

    def GotoDate(self):
        # =>init vars
        gyear = 0
        gmonth = 0
        gday = 0
        # =>debug mode
        if Glob.DEBUG_MODE:
            print('goto')
        # =>split date
        date = Glob.options['goto'].split('.')
        gyear = int(date[0])
        gmonth = int(date[1])
        gday = int(date[2])
        # =>validate persian date
        if not common.PCAL_ValidateJalaliDate(gyear, gmonth, gday):
            display.PCAL_RaiseError(
                'bad persian date format : '+Glob.options['goto'])
        # =>print goto date
        display.PCAL_DisplayGotoDate({'y': gyear, 'm': gmonth, 'd': gday})
    # =============================================

    def SetEvent(self):
        if Glob.DEBUG_MODE:
            print('set-event')
        # TODO:
    # =============================================

    def current(self):
        if Glob.DEBUG_MODE:
            print('current')
        # =>if current option is day
        if Glob.options['current'] == 'day':
            display.PCAL_DisplayToday()
        # =>if current option is month
        elif Glob.options['current'] == 'month':
            display.PCAL_DisplayMonth()
        # =>if current option is year
        elif Glob.options['current'] == 'year':
            display.PCAL_DisplayYear()


# =============================================
# =>main function
if __name__ == '__main__':
    # print('Welcome To PCAL')
    pcal = PCAL()
