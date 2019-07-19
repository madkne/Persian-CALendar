import _global as Glob
import datetime
import io
import os

import convert
import common
# -----------------------------------------
fa = {
    'lang': 'fa',
    'months': ["فروردین", "اردیبهشت", "خرداد", "تیر", "مرداد",
               "شهریور", "مهر", "آبان", "آذر", "دی", "بهمن", "اسفند"],
    'weekdays': ["شنبه", "یکشنبه", "دوشنبه",
                 "سه شنبه", "چهارشنبه", "پنج شنبه", "جمعه"],
    'dictionary': {'today': 'امروز', 'equal': 'برابر با', 'leapyear': 'سال کبیسه', 'thatday': 'آن روز', 'interval': 'فاصله تاریخی', 'days': 'روز', 'daysago': 'روز پیش', 'dayslater': 'روز بعد', 'and': 'و', 'years': 'سال', 'months': 'ماه', 'ago': 'پیش', 'later': 'بعد', 'events': 'رویداد ها', 'personal': 'شخصی', 'holiday': 'تعطیل', 'occasion': 'مناسبت', 'no_event_thisday': 'هیچ رویدادی در این روز وجود ندارد', 'no_event_thismonth': 'هیچ رویدادی در این ماه وجود ندارد'}
}
# -----------------------------------------
en = {
    'lang': 'en',
    'months': ['Farvardin', 'Ordibehesht', 'Khordad', 'Tir', 'Mordad',
               'Shahrivar', 'Mehr', 'Aban', 'Azar', 'Dey', 'Bahman', 'Esfand'],
    'weekdays': ['Shanbe', 'Yekshanbe', 'Doshanbe',
                 'Seshanbe', 'Chahârshanbe', 'Panjshanbe', 'jomøe'],
    'dictionary': {'today': 'Today', 'equal': 'Equal', 'leapyear': 'Leap Year', 'thatday': 'That Day', 'interval': 'Date interval', 'days': 'Day(s)', 'daysago': 'Day(s) ago', 'dayslater': 'Day(s) later', 'and': 'and', 'years': 'Year(s)', 'months': 'Month(s)', 'ago': 'ago', 'later': 'later', 'events': 'Events', 'personal': 'Personal', 'holiday': 'Holiday', 'occasion': 'Occasion', 'no_event_thisday': 'There are no events on this day', 'no_event_thismonth': 'There are no events on this month'}
}


# =============================================
def PCAL_DisplayGotoDate(jalalidate):
    """
    extensions to use:
    persian [OK] , english [OK] , info [OK] , events [OK]
    """
    # =>init vars
    lang = None
    lg = None
    weekday = 0
    interval = 0
    postinterval = 'days'
    # =>check lang option
    lg = Glob.options['lang']
    if lg == 'fa':
        lang = fa
    elif lg == 'en':
        lang = en
    # =>if info is true
    if Glob.options['info'] == 'true':
        # =>print calendar
        __DisplayMonthCalendar(jalalidate, lang)
        # =>convert jalali to gregory
        gregory = convert.JalaliToGregorian(
            jalalidate['y'], jalalidate['m'], jalalidate['d'])
        endate = gregory.getGregorianList()
        # =>get weekday
        goto = datetime.datetime(endate['y'], endate['m'], endate['d'])
        weekday = common.PCAL_NormalizeWeekday(goto.weekday())
        # =>calc interval
        today = datetime.datetime.today()
        interval = common.PCAL_CalculateInterval(
            {'y': today.year, 'm': today.month, 'd': today.day}, endate)
        # print(interval)
        # =>check if year is leap
        leapyear = ''
        if common.PCAL_IsLeapYear(jalalidate['y']):
            leapyear = "({})".format(lang['dictionary']['leapyear'])
        # =>print info
        print("{} {} {} {} {} {} {} {}\n{}".format(
            lang['dictionary']['thatday'],
            lang['weekdays'][weekday],
            common.PCAL_LocalNumber(jalalidate['d'], lg),
            lang['months'][jalalidate['m']-1],
            common.PCAL_LocalNumber(jalalidate['y'], lg),
            lang['dictionary']['equal'],
            "{}/{}/{}".format(endate['y'], endate['m'], endate['d']),
            leapyear,
            "{} : {}".format(lang['dictionary']['interval'], common.PCAL_CalculateHumanlyInterval(
                interval, lang, interval['sign']))
        ))

    else:
        __DisplayMonthCalendar(jalalidate, lang)
    #=>if event is true
    if Glob.options['event'] == 'true':
        print()
        PCAL_DisplayEventsList(jalalidate,lang)
# =============================================


def PCAL_DisplayToday():
    """
    extensions to use:
    persian [OK] , english [OK] , info [OK] , events [OK]
    """
    # =>init vars
    lang = None
    jalalidate = {}
    tablecol1 = []
    tablecol2 = []
    maxcol1width = 10
    # =>get today from datetime
    today = datetime.datetime.today()
    # =>convert datetime to jalali
    jalali = convert.GregorianToJalali(
        today.year, today.month, today.day, today.weekday())
    jalalidate = jalali.getJalaliList()
    if Glob.DEBUG_MODE:
        print(jalalidate)
    # =>check lang option
    lg = Glob.options['lang']
    if lg == 'fa':
        lang = fa
    elif lg == 'en':
        lang = en
    # =>if info is true
    if Glob.options['info'] == 'true':
        # =>check if year is leap
        leapyear = ''
        if common.PCAL_IsLeapYear(jalalidate['y']):
            leapyear = "({})".format(lang['dictionary']['leapyear'])
        # =>print info
        print("{} {} {} {} {} {} {} {}".format(
            lang['dictionary']['today'],
            lang['weekdays'][jalalidate['w']],
            common.PCAL_LocalNumber(jalalidate['d'], lg),
            lang['months'][jalalidate['m']-1],
            common.PCAL_LocalNumber(jalalidate['y'], lg),
            lang['dictionary']['equal'],
            "{}/{}/{}".format(today.year, today.month, today.day),
            leapyear
        ))

    else:
        print("{}/{}/{}".format(
            common.PCAL_LocalNumber(jalalidate['y'], lg),
            common.PCAL_LocalNumber(jalalidate['m'], lg),
            common.PCAL_LocalNumber(jalalidate['d'], lg)))

    # =>if event is true
    if Glob.options['event'] == 'true':
        print()
        PCAL_DisplayEventsList(jalalidate,lang)
# =============================================


def PCAL_DisplayTable(header, col1, col2, maxcol1width=50, margin=2, hassplitline=True, usingcolors=True,color1=None):
    # print('color1:',color1)
    # =>get width, height of terminal
    rows, columns = os.popen('stty size', 'r').read().split()
    if Glob.DEBUG_MODE:
        print(rows, columns)
    # init vars
    draw = ''
    startmargin = 0
    headerlen = len(header)
    leftborder = 2
    TopBorderChar = '\u2500'
    LeftBorderChar = '\u2502'
    RightBorderChar = '\u2502'
    BottomBorderChar = '\u2500'
    CenterBorderChar = '\u2502'
    BottomLeftCornerChar = '\u2514'
    BottomRightCornerChar = '\u2518'
    BottomCenterCornerChar = '\u2534'
    TopLeftCornerChar = '\u250C'
    TopRightCornerChar = '\u2510'
    TopCenterCornerChar = '\u252C'
    emptyfirstcolumn = ''
    col1width = maxcol1width+margin+1
    col2width = int(columns)-margin-col1width-2
    hline = ''
    # =>make hline for rows
    if hassplitline:
        if usingcolors:
            hline += Glob.TerminalColors.CYANBOLD
        startmargin = margin
        isleftborder = False
        for i in range(0, int(columns)-margin, 1):
            # =>set left margin as start
            if startmargin > 0:
                hline += ' '
                startmargin -= 1
            # =>draw left border
            elif not isleftborder:
                hline += '\u251C'
                isleftborder = True
            # draw center border
            elif i == col1width:
                hline += '\u253C'
            # =>fill the other spaces with '-'
            elif i < int(columns)-margin-1:
                hline += TopBorderChar
            # =>draw right border
            else:
                hline += '\u2524'
        hline += Glob.TerminalColors.NORMAL
    # -----------------------------------
    # =>draw header on table
    startmargin = margin
    lenght = len(header)
    tmpleftborder = leftborder
    isleftcorner = False
    isrightcorner = False
    iscentercorner = False
    for i in range(0, int(columns)-margin, 1):
        # =>set left margin as start
        if startmargin > 0:
            draw += ' '
            startmargin -= 1
        # =>draw left corner
        elif not isleftcorner:
            draw += TopLeftCornerChar
            isleftcorner = True
        # => draw top left border before header text
        elif tmpleftborder > 0:
            if usingcolors:
                draw += Glob.TerminalColors.CYANBOLD
            draw += TopBorderChar
            draw += Glob.TerminalColors.NORMAL
            tmpleftborder -= 1
        # =>draw center corner
        elif i == col1width and not iscentercorner:
            draw += TopCenterCornerChar
            iscentercorner = True
        # =>set header text
        elif lenght > 0:
            if usingcolors:
                draw += Glob.TerminalColors.GREENBOLD
            draw += header[headerlen-lenght]
            draw += Glob.TerminalColors.NORMAL
            lenght -= 1
        # =>fill the other spaces with '-'
        elif i < int(columns)-margin-1:
            if usingcolors:
                draw += Glob.TerminalColors.CYANBOLD
            draw += TopBorderChar

        # =>draw right corner
        elif not isrightcorner:
            draw += TopRightCornerChar
            isrightcorner = True
            draw += Glob.TerminalColors.NORMAL
    print(draw)
    # -----------------------------------
    #=>draw rows
    #=>draw left border
    for i in range(0, len(col1), 1):
        # =>init vars
        emptyfirstcolumn = ''
        len1 = len(col1[i])
        # print(len1,col1width)
        len2 = len(col2[i])
        # if len2<col2width: len2=col2width
        draw = ''
        startmargin = margin
        isleftborder = False
        # .........................
        # =>draw col1 text
        for j in range(0, col1width, 1):
            # =>set left margin as start
            if startmargin > 0:
                draw += ' '
                emptyfirstcolumn += ' '
                startmargin -= 1
            elif not isleftborder:
                if usingcolors:
                    draw += Glob.TerminalColors.CYANBOLD
                    emptyfirstcolumn += Glob.TerminalColors.CYANBOLD
                draw += LeftBorderChar
                emptyfirstcolumn += LeftBorderChar
                draw += Glob.TerminalColors.NORMAL
                emptyfirstcolumn += Glob.TerminalColors.NORMAL
                isleftborder = True
                #=>set custom color for col1 text
                if color1!=None and i<len(color1):
                    draw+=color1[i]
                #=>set bright color for col1 text
                elif usingcolors:
                    draw += Glob.TerminalColors.BRIGHT
            # =>set col1 text
            elif len1 > 0:
                char=col1[i][len(col1[i])-len1]
                draw += char
                emptyfirstcolumn += ' '
                len1 -= 1
            # =>fill the other spaces of col1 with ' '
            else:
                draw += Glob.TerminalColors.NORMAL
                emptyfirstcolumn += ' '
                draw += ' '
        # =>draw column line
        draw += Glob.TerminalColors.NORMAL
        if usingcolors:
            draw += Glob.TerminalColors.CYANBOLD
            emptyfirstcolumn += Glob.TerminalColors.CYANBOLD
        draw += CenterBorderChar
        emptyfirstcolumn += CenterBorderChar
        draw += Glob.TerminalColors.NORMAL
        emptyfirstcolumn += Glob.TerminalColors.NORMAL
        # .........................
        tmplen2 = len(col2)
        # =>draw col2 text
        for j in range(0, int(len2/col2width)+1, 1):
            # =>get col2 segment for draw in this row, and the other in next rows!
            col2seg = col2[i][j*col2width:col2width+(j*col2width)]
            # =>if more than one row
            if j > 0:
                if usingcolors:
                    draw += Glob.TerminalColors.CYANBOLD
                print(draw+RightBorderChar)
                draw = emptyfirstcolumn
            # print('col2seg:',col2seg)
            tmplen2 = len(col2seg)
            for k in range(0, col2width, 1):
                # =>set col2 text
                if tmplen2 > 0:
                    draw += col2seg[len(col2seg)-tmplen2]
                    tmplen2 -= 1
                # =>fill the other spaces of col2 with ' '
                else:
                    draw += ' '
        # =>draw column line
        if usingcolors:
            draw += Glob.TerminalColors.CYANBOLD
        draw += RightBorderChar
        draw += Glob.TerminalColors.NORMAL
        # =>print row
        print(draw)
        if hassplitline and i < len(col1)-1:
            print(hline)
    # =>draw bottom line
    draw = ''
    startmargin = margin
    isleftcorner = False
    isrightcorner = False
    iscentercorner = False
    if usingcolors:
        draw += Glob.TerminalColors.CYANBOLD

    for i in range(0, int(columns)-margin, 1):
        # =>set left margin as start
        if startmargin > 0:
            draw += ' '
            startmargin -= 1
        # =>draw left corner
        elif not isleftcorner:
            draw += BottomLeftCornerChar
            isleftcorner = True
        # =>draw left corner
        elif i == col1width and not iscentercorner:
            draw += BottomCenterCornerChar
            iscentercorner = True
        # =>fill the all spaces with '-'
        elif i < int(columns)-margin-1:
            draw += BottomBorderChar
        # =>draw left corner
        elif not isrightcorner:
            draw += BottomRightCornerChar
            isrightcorner = True
    draw += Glob.TerminalColors.NORMAL
    print(draw)


# =============================================
def PCAL_DisplayMonth():
    """
    extensions to use:
    persian [OK] , english [OK] , events [OK]
    """
    # =>init vars
    lang = None
    maxdays = 0
    tablecol1 = []
    tablecol2 = []
    colorcol1=[]
    maxcol1width = 10
    # =>check lang option
    lg = Glob.options['lang']
    if lg == 'fa':
        lang = fa
    elif lg == 'en':
        lang = en
     # =>get curent month from datetime
    today = datetime.datetime.today()
    # =>convert datetime to jalali
    jalali = convert.GregorianToJalali(
        today.year, today.month, today.day)
    jalalidate = jalali.getJalaliList()
    # =>get maxdays of month
    maxdays = common.PCAL_ReturnDaysFromJalaliMonth(
        jalalidate['m'], jalalidate['y'])
    # =>print month calendar
    __DisplayMonthCalendar(jalalidate, lang)
    # =>if event is true
    if Glob.options['event'] == 'true':
        for i in range(0, maxdays, 1):
            # =>get all events of day
            retdata = PCAL_DisplayEventsList(
                {'y': jalalidate['y'], 'm': jalalidate['m'], 'd': i}, lang, maxcol1width, 'month', False)
            #=>if tablecol1 not empty, then append!
            if len(retdata['tablecol1']) > 0:
                if Glob.DEBUG_MODE:
                    print(i, retdata)
                #=>append item by item from retdata['tablecol1']
                for con in retdata['tablecol1']:
                    tablecol1.append(con)
                #=>append item by item from retdata['colorcol1']
                for con in retdata['colorcol1']:
                    colorcol1.append(con)
                #=>append item by item from retdata['tablecol2']
                for con in retdata['tablecol2']:
                    tablecol2.append(con)
                #=>update maxcol1width var
                maxcol1width = retdata['maxcol1width']
        # =>draw table if exist any events
        if len(tablecol1) > 0:
            PCAL_DisplayTable(
                lang['dictionary']['events'], tablecol1, tablecol2, maxcol1width,color1=colorcol1)
        # =>if not any event, then print message
        else:
            print(lang['dictionary']['no_event_thismonth'])
# =============================================


def PCAL_DisplayEventsList(jalalidate, lang, maxcol1width=10, mode='day', drawtable=True):
    # =>init vars
    tablecol1 = []
    tablecol2 = []
    colorcol1=[]
    lg = lang['lang']
    # =>get events list of day
    events = common.PCAL_ReturnEventsFromJalaliDay(
        jalalidate['y'], jalalidate['m'],  jalalidate['d'])
    # =>fill col1,col2 of table
    for i in range(0, len(events), 1):
        col1 = ''
        colord=''
        #=>check type of event day for set a good color
        if events[i]['type']=='personal':
            colord=Glob.PERSONAL_EVENT_COLOR
        # =>if day is holiday or jomøe (holiday by default)
        elif events[i]['type']=='holiday':
            colord=Glob.HOLIDAY_EVENT_COLOR
        # =>if day is occasion
        elif events[i]['type']=='occasion':
            colord=Glob.OCCASION_EVENT_COLOR
        else:
            colord=Glob.TerminalColors.NORMAL
        #=>check if mode is month
        if mode == 'month':
            # =>make col1 text from type of event file and month and day date
            col1 = "{} {} ({})".format(common.PCAL_LocalNumber(jalalidate['d'], lg),
                                        lang['months'][jalalidate['m']-1], lang['dictionary'][events[i]['type']])
        # =>if mode is day
        elif mode == 'day':
            # =>make col1 text from name and type of event file
            col1 = "{} ({})".format(events[i]['name'].split('.')[0],
                                     lang['dictionary'][events[i]['type']])
        # =>reassign max col1 width for draw table
        if len(col1) > maxcol1width:
            maxcol1width = len(col1)
        #=> append to colorcol1 list, color of col1
        colorcol1.append(colord)
        # =>append to tablecol1,tablecol2 lists
        tablecol1.append(col1)
        tablecol2.append(events[i]['text'])
    # =>draw table if exist any events and if drawtable is true
    if drawtable:
        if len(tablecol1) > 0:
            PCAL_DisplayTable(
                lang['dictionary']['events'], tablecol1, tablecol2, maxcol1width,color1=colorcol1)
        # =>if not any event, then print message
        else:
            print(lang['dictionary']['no_event_thisday'])
    # =>if drawtable is false, then return all
    else:
        return {'maxcol1width': maxcol1width, 'tablecol1': tablecol1, 'tablecol2': tablecol2,'colorcol1':colorcol1}
# =============================================


def PCAL_DisplayYear():
    """
    extensions to use:
    persian [OK] , english [OK]
    """
    # =>init vars
    lang = None
    months = []
    maxcols = 3
    splitwidth = '    '  # 4 spaces
    monthindex = 0
    maxcalendarheight = 8
    calendarwidth = 21
    # =>check lang option
    lg = Glob.options['lang']
    if lg == 'fa':
        lang = fa
    elif lg == 'en':
        lang = en
     # =>get curent year from datetime
    today = datetime.datetime.today()
    # =>convert datetime to jalali
    jalali = convert.GregorianToJalali(
        today.year, today.month, today.day)
    jalalidate = jalali.getJalaliList()
    # =>#TODO:
    for i in range(1, 13, 1):
        # =>create new date for next month for printing
        if i == jalalidate['m']:
            nextmonthdate = {
                'y': jalalidate['y'], 'm': i, 'd': jalalidate['d']}
        else:
            nextmonthdate = {'y': jalalidate['y'], 'm': i, 'd': 0}
        # =>get month calendar as string, no print it!
        months.append(__DisplayMonthCalendar(
            nextmonthdate, lang, "string").split('\n'))
    # =>print year on center
    yeartitle = str(common.PCAL_LocalNumber(jalalidate['y'], lg))
    totalwidth = calendarwidth*maxcols+len(splitwidth)*maxcols-len(splitwidth)
    print(Glob.TerminalColors.GREENBOLD+yeartitle.center(totalwidth, ' '))
    print('----::::::::::----'.center(totalwidth, ' ') +
          '\n'+Glob.TerminalColors.NORMAL)
    # =>print month calendars in 3x4 cols and rows
    for i in range(0, int(12/maxcols), 1):
        row = ''
        # =>TODO:
        for k in range(0, maxcalendarheight, 1):
            for j in range(0, maxcols, 1):
                if k >= len(months[monthindex+j]) or len(months[monthindex+j][k]) == 0:
                    row += ''.center(calendarwidth, ' ')
                else:
                    row += months[monthindex+j][k]
                row += splitwidth
            row += '\n'
        print(row)
        monthindex += maxcols


# =============================================
def __DisplayMonthCalendar(jalalidate, lang, mode="print"):
    # =>init vars
    calendarwidth = 20
    maxheight = 6
    daymonth = 0
    lastday = 0
    startweekday = 0
    output = io.StringIO()
    lg = lang['lang']
    today = datetime.datetime.today()
    # =>get startweekday
    gregory = convert.JalaliToGregorian(jalalidate['y'], jalalidate['m'], 1)
    gregorylist = gregory.getGregorianList()
    firstday = today.replace(
        year=gregorylist['y'], month=gregorylist['m'], day=gregorylist['d'])
    startweekday = common.PCAL_NormalizeWeekday(firstday.weekday())
    # =>get lastday
    # =>test for 30
    if not common.PCAL_ValidateJalaliDate(jalalidate['y'], jalalidate['m'], 30):
        lastday = 29
    # =>test for 31
    elif not common.PCAL_ValidateJalaliDate(jalalidate['y'], jalalidate['m'], 31):
        lastday = 30
    else:
        lastday = 31
    # =>print for debug mode
    if Glob.DEBUG_MODE:
        print(jalalidate, firstday, lastday, startweekday, gregorylist)
    # =>print in center month name
    monthname = "{} {}".format(
        lang['months'][jalalidate['m']-1], common.PCAL_LocalNumber(jalalidate['y'], lg))
    print(Glob.TerminalColors.CYANBOLD+monthname.center(calendarwidth,
                                                        ':')+Glob.TerminalColors.NORMAL, end=' \n', file=output)
    # print weekdays names
    print(Glob.TerminalColors.OKBLUE, end='', file=output)
    for i in range(0, 7, 1):
        print(lang['weekdays'][i][0:2], sep='', end=' ', file=output)
    print(Glob.TerminalColors.NORMAL, end='', file=output)
    # print('\n'+''.center(width,'-'))
    print(file=output)
    # =>print month days
    for i in range(0, maxheight, 1):
        for j in range(0, 7, 1):
            # =>print empty if is before startweekday or after lastday
            if (daymonth == 0 and j < startweekday) or (daymonth == lastday):
                print('  ', end=' ', file=output)
            else:
                daymonth += 1
                eventtype = common.PCAL_ReturnEventsFromJalaliDay(
                    jalalidate['y'], jalalidate['m'], daymonth, True)
                # =>if day is current day, then selected by blue color
                if daymonth == jalalidate['d']:
                    print(Glob.TerminalColors.WHITEBLUE, end='', file=output)
                # =>if day is personal
                elif eventtype == 'personal':
                    print(Glob.PERSONAL_EVENT_COLOR, end='', file=output)
                # =>if day is holiday or jomøe (holiday by default)
                elif j == 6 or eventtype == 'holiday':
                    print(Glob.HOLIDAY_EVENT_COLOR, end='', file=output)
                # =>if day is occasion
                elif eventtype == 'occasion':
                    print(Glob.OCCASION_EVENT_COLOR, end='', file=output)
                # =>print day of month
                print('{:>2}'.format(common.PCAL_LocalNumber(
                    daymonth, lg)), end='', file=output)
                # =>set normal style
                print(Glob.TerminalColors.NORMAL, end=' ', file=output)

        # =>go to new line
        print(file=output)
        # =>check if end day
        if daymonth >= lastday:
            break

    # =>print output or return output
    if mode == 'print':
        print(output.getvalue())
    elif mode == 'string':
        return output.getvalue()
    output.close()


# =============================================


# =============================================


def PCAL_RaiseError(msg):
    print("PCAL:ERROR:{}".format(msg))
