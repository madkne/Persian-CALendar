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
    'dictionary': {'today': 'امروز', 'equal': 'برابر با', 'leapyear': 'سال کبیسه','thatday':'آن روز','interval':'فاصله تاریخی','days':'روز','daysago':'روز پیش','dayslater':'روز بعد','and':'و','years':'سال','months':'ماه','ago':'پیش','later':'بعد'}
}
# -----------------------------------------
en = {
    'lang': 'en',
    'months': ['Farvardin', 'Ordibehesht', 'Khordad', 'Tir', 'Mordad',
               'Shahrivar', 'Mehr', 'Aban', 'Azar', 'Dey', 'Bahman', 'Esfand'],
    'weekdays': ['Shanbe', 'Yekshanbe', 'Doshanbe',
                 'Seshanbe', 'Chahârshanbe', 'Panjshanbe', 'jomøe'],
    'dictionary': {'today': 'Today', 'equal': 'Equal', 'leapyear': 'Leap Year','thatday':'That Day','interval':'Date interval','days':'Day(s)','daysago':'Day(s) ago','dayslater':'Day(s) later','and':'and','years':'Year(s)','months':'Month(s)','ago':'ago','later':'later'}
}



# =============================================
def PCAL_DisplayGotoDate(jalalidate):
    """
    extensions to use:
    persian [..] , english [..] , info [..] , events [..] TODO:
    """
    # =>init vars
    lang = None
    lg = None
    weekday=0
    interval=0
    postinterval='days'
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
        #=>get weekday
        goto=datetime.datetime(endate['y'],endate['m'],endate['d'])
        weekday = common.PCAL_NormalizeWeekday(goto.weekday())
        #=>calc interval
        today=datetime.datetime.today()
        interval=common.PCAL_CalculateInterval({'y':today.year,'m':today.month,'d':today.day},endate)
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
            "{} : {}".format(lang['dictionary']['interval'],common.PCAL_CalculateHumanlyInterval(interval,lang,interval['sign']))
        ))

    else:
        __DisplayMonthCalendar(jalalidate, lang)
# =============================================


def PCAL_DisplayToday():
    """
    extensions to use:
    persian [OK] , english [OK] , info [OK] , events [..] TODO:
    """
    # =>init vars
    lang = None
    jalalidate = {}
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
# =============================================
def PCAL_DisplayTable(header,col1,col2,maxcol1width=50,margin=2,hassplitline=True,usingcolors=True):
    #=>get width, height of terminal
    rows, columns = os.popen('stty size', 'r').read().split()
    if Glob.DEBUG_MODE: print(rows,columns)
    #init vars
    draw=''
    startmargin=0
    headerlen=len(header)
    leftborder=2
    TopBorderChar='\u2500'
    LeftBorderChar='\u2502'
    RightBorderChar='\u2502'
    BottomBorderChar='\u2500'
    CenterBorderChar='\u2502'
    BottomLeftCornerChar='\u2514'
    BottomRightCornerChar='\u2518'
    BottomCenterCornerChar='\u2534'  
    TopLeftCornerChar='\u250C'
    TopRightCornerChar='\u2510'
    TopCenterCornerChar='\u252C'  
    emptyfirstcolumn=''
    col1width=maxcol1width+margin+1
    col2width=int(columns)-margin-col1width-2
    hline=''
    #=>make hline for rows
    if hassplitline:
        if usingcolors: hline+=Glob.TerminalColors.CYANBOLD
        startmargin=margin
        isleftborder=False
        for i in range(0,int(columns)-margin,1):
            #=>set left margin as start
            if startmargin>0: 
                hline+=' '
                startmargin-=1
            #=>draw left border
            elif not isleftborder:
                hline+='\u251C'
                isleftborder=True
            #draw center border
            elif i==col1width:
                hline+='\u253C'
            #=>fill the other spaces with '-'
            elif i<int(columns)-margin-1:
                hline+=TopBorderChar
            #=>draw right border
            else: hline+='\u2524'
        hline+=Glob.TerminalColors.NORMAL
    #-----------------------------------
    #=>draw header on table
    startmargin=margin
    lenght=len(header)
    tmpleftborder=leftborder
    isleftcorner=False
    isrightcorner=False
    iscentercorner=False
    for i in range(0,int(columns)-margin,1):
        #=>set left margin as start
        if startmargin>0: 
            draw+=' '
            startmargin-=1
        #=>draw left corner
        elif not isleftcorner:
            draw+=TopLeftCornerChar
            isleftcorner=True    
        #=> draw top left border before header text 
        elif tmpleftborder>0:
            if usingcolors: draw+=Glob.TerminalColors.CYANBOLD
            draw+=TopBorderChar
            draw+=Glob.TerminalColors.NORMAL
            tmpleftborder-=1
        #=>draw center corner
        elif i==col1width and not iscentercorner:
            draw+=TopCenterCornerChar
            iscentercorner=True 
        #=>set header text
        elif lenght>0:
            if usingcolors: draw+=Glob.TerminalColors.GREENBOLD
            draw+=header[headerlen-lenght] 
            draw+=Glob.TerminalColors.NORMAL
            lenght-=1
        #=>fill the other spaces with '-'
        elif i<int(columns)-margin-1:
            if usingcolors: draw+=Glob.TerminalColors.CYANBOLD
            draw+=TopBorderChar
            
        #=>draw right corner
        elif not isrightcorner:
            draw+=TopRightCornerChar
            isrightcorner=True 
            draw+=Glob.TerminalColors.NORMAL
    print(draw)
    #-----------------------------------
    # =>draw rows
    #draw left border
    for i in range(0,len(col1),1):
        #=>init vars
        emptyfirstcolumn=''
        len1=len(col1[i])
        len2=len(col2[i])
        # if len2<col2width: len2=col2width
        draw=''
        startmargin=margin
        isleftborder=False
        #.........................
        #=>draw col1 text
        for j in range(0,col1width,1):
            #=>set left margin as start
            if startmargin>0: 
                draw+=' '
                emptyfirstcolumn+=' '
                startmargin-=1
            elif not isleftborder:
                if usingcolors: 
                    draw+=Glob.TerminalColors.CYANBOLD
                    emptyfirstcolumn+=Glob.TerminalColors.CYANBOLD
                draw+=LeftBorderChar
                emptyfirstcolumn+=LeftBorderChar
                draw+=Glob.TerminalColors.NORMAL
                emptyfirstcolumn+=Glob.TerminalColors.NORMAL
                isleftborder=True
            #=>set col1 text
            elif len1>0:
                if usingcolors: draw+=Glob.TerminalColors.BRIGHT
                draw+=col1[i][len(col1[i])-len1] 
                draw+=Glob.TerminalColors.NORMAL
                emptyfirstcolumn+=' '
                len1-=1
            # =>fill the other spaces of col1 with ' '
            else:
                emptyfirstcolumn+=' '
                draw+=' '
        #=>draw column line
        if usingcolors: 
            draw+=Glob.TerminalColors.CYANBOLD
            emptyfirstcolumn+=Glob.TerminalColors.CYANBOLD
        draw+=CenterBorderChar
        emptyfirstcolumn+=CenterBorderChar
        draw+=Glob.TerminalColors.NORMAL
        emptyfirstcolumn+=Glob.TerminalColors.NORMAL
        #.........................
        tmplen2=len(col2)
        #=>draw col2 text
        for j in range(0,int(len2/col2width)+1,1):
            #=>get col2 segment for draw in this row, and the other in next rows!
            col2seg=col2[i][j*col2width:col2width+(j*col2width)]
            #=>if more than one row
            if j>0:
                if usingcolors: draw+=Glob.TerminalColors.CYANBOLD
                print(draw+RightBorderChar)
                draw=emptyfirstcolumn
            # print('col2seg:',col2seg)
            tmplen2=len(col2seg)
            for k in range(0,col2width,1):
                # =>set col2 text
                if tmplen2>0:
                    draw+=col2seg[len(col2seg)-tmplen2] 
                    tmplen2-=1
                # =>fill the other spaces of col2 with ' '
                else:
                    draw+=' '
        #=>draw column line
        if usingcolors: draw+=Glob.TerminalColors.CYANBOLD
        draw+=RightBorderChar
        draw+=Glob.TerminalColors.NORMAL
        #=>print row
        print(draw)
        if hassplitline and i<len(col1)-1:
            print(hline)
    #=>draw bottom line
    draw=''
    startmargin=margin
    isleftcorner=False
    isrightcorner=False
    iscentercorner=False
    if usingcolors: draw+=Glob.TerminalColors.CYANBOLD
            
    for i in range(0,int(columns)-margin,1):
        #=>set left margin as start
        if startmargin>0: 
            draw+=' '
            startmargin-=1
        #=>draw left corner
        elif not isleftcorner:
            draw+=BottomLeftCornerChar
            isleftcorner=True 
        #=>draw left corner
        elif i==col1width and not iscentercorner:
            draw+=BottomCenterCornerChar
            iscentercorner=True    
        #=>fill the all spaces with '-'
        elif i<int(columns)-margin-1:
            draw+=BottomBorderChar
        #=>draw left corner
        elif not isrightcorner:
            draw+=BottomRightCornerChar
            isrightcorner=True  
    draw+=Glob.TerminalColors.NORMAL
    print(draw)



# =============================================
def PCAL_DisplayMonth():
    """
    extensions to use:
    persian [OK] , english [OK] , events [..] TODO:
    """
    # =>init vars
    lang = None
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
    # =>print month calendar
    __DisplayMonthCalendar(jalalidate, lang)

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
        #=>TODO:
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
                # =>if day is current day, then selected by blue color
                if daymonth == jalalidate['d']:
                    print(Glob.TerminalColors.WHITEBLUE, end='', file=output)
                # =>if day is jomøe (holiday by default)
                if j == 6:
                    print(Glob.TerminalColors.REDBOLD, end='', file=output)
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
