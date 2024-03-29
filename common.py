import datetime
import _global as Glob
import os
import json
# -----------------------------------------
numbers = {
    'fa': ['۰', '۱', '۲', '۳', '۴', '۵', '۶', '۷', '۸', '۹', '۱۰']
}
# -----------------------------------------
leaps = [
    '1308', '1313', '1317', '1321', '1325', '1329', '1333', '1337', '1341', '1346', '1350', '1354', '1358', '1362', '1366', '1370', '1375', '1379', '1383', '1387', '1391', '1399', '1403', '1408', '1412', '1416', '1420'
]
# =============================================


def PCAL_IsLeapYear(year):
    for i in leaps:
        if int(i) == year:
            return True
    return False

# =============================================


def PCAL_NormalizeWeekday(weekday):
    # =>weekday (gor=>jal) where Monday == 0 ... Sunday == 6.
    fixed = weekday
    for i in range(0, 2, 1):
        if fixed+1 == 7:
            fixed = 0
        else:
            fixed += 1
    return fixed

# =============================================


def PCAL_ValidateJalaliDate(year, month, day):
    """
    year:1300..1500
    month:1..12
    day:1..31
    """
    # =>check month and year and day limit
    if month < 1 or month > 12 or year < 1300 or year > 1420 or day < 1 or day > 31:
        return False
    # =>check day for 6 basic months (lastday:31)
    if month < 7 and day > 31:
        return False
    # =>check day for 5 secondary months (lastday:30)
    elif month > 6 and month < 12 and day > 30:
        return False
    # =>check day for last month (lastday:29|30[leap])
    elif month == 12:
        isleap = PCAL_IsLeapYear(year)
        if isleap and day > 30:
            return False
        elif not isleap and day > 29:
            return False
    # =>else return true!
    return True


# =============================================
def PCAL_LocalNumber(num, lang):
    if lang == 'en':
        return num
    else:
        ret = ''
        for i in str(num):
            ret += numbers[lang][int(i)]
        return ret
# =============================================


def PCAL_CalculateInterval(startdt, enddt):
    """
    startdt,enddt:gregory:['y'],['m'],['d']
    """
    # =>init vars
    sign = True
    months = 0
    # =>get start date and end date from datetime to get their timestamps
    stdt = datetime.datetime(startdt['y'], startdt['m'], startdt['d'])
    endt = datetime.datetime(enddt['y'], enddt['m'], enddt['d'])
    # =>get timestamps
    stimestamp = stdt.timestamp()
    etimestamp = endt.timestamp()
    # =>calc interval by end date timestamp and start date timestamp
    interval = (etimestamp-stimestamp)
    # =>if interval is negative, then False sign and positive interval
    if interval < 0:
        sign = False
        interval *= -1
    # =>calc total days from interval divides
    days = int(interval/60/60/24)
    # =>define current month and year to set by start date
    curyear = startdt['y']
    curmonth = startdt['m']
    # =>loop for subtract from days and and to months
    while True:
        # =>calc count days of current month
        d = PCAL_ReturnDaysFromJalaliMonth(curmonth, curyear)
        # =>stop condition! if count days of month is bigger than total days
        if d > days:
            break
        # =>add one to months and subtract 'd' from days
        months += 1
        days -= d
        # =>reassign(update) curyear,curmonth by add one month to current date(start date)
        curdate = {'y': curyear, 'm': curmonth}
        curdate = PCAL_AddToJalaliDate(curdate, 1, 'm')
        curyear = curdate['y']
        curmonth = curdate['m']
    # print('tmp:', months, days)
    # =>calc years by months, recalc months
    years = int(months/12)
    months = months % 12
    # =>return interval as a date with sign of date
    return {'y': years, 'm': months, 'd': days, 'sign': sign}
# =============================================


def PCAL_AddToJalaliDate(current, add=1, mode='d'):
    """
    current:{'y','m','d'}
    add:65
    mode:'d'|'m'|'y'
    """
    if Glob.DEBUG_MODE:
        print(current, add, mode)
    # =>if add mode is day
    if mode == 'd':
        # =>divide days to 28 (less than 1 month)
        daysdivide = int(add/28)
        if daysdivide < add/28:
            daysdivide += 1
        # =>iterate by daysdivide, and ‍every time just add 28 days or less!
        for i in range(0, daysdivide, 1):
            # =>calc tmp add, if bigger than 28, set 28, else tmpadd
            tmpadd = add-(i*28)
            if tmpadd > 28:
                tmpadd = 28
            # =>add to current day,tmpadd!
            current['d'] += tmpadd
            # =>check is bigger than 29,30,31 days
            maxdays = PCAL_ReturnDaysFromJalaliMonth(
                current['m'], current['y'])
            if current['d'] > maxdays:
                # =>get different and add one to month
                diff = current['d']-maxdays
                current['m'] += 1
                # =>calc year and month by diff
                current['m'] += int(diff/maxdays)
                current['d'] = diff % maxdays
                # print(diff, maxdays)
                # =>check is bigger than 12 months
                if current['m'] > 12:
                    # =>get different and add one to year
                    diff = current['m']-12
                    current['y'] += 1
                    # =>calc year and month by diff
                    current['y'] += int(diff/12)
                    current['m'] = diff % 12

    # =>else if add mode is month
    elif mode == 'm':
        current['m'] += add
        # =>if was bigger than 12 months
        if current['m'] > 12:
            # =>get different and add one to year
            diff = current['m']-12
            current['y'] += 1
            # =>calc year and month by diff
            current['y'] += int(diff/12)
            current['m'] = diff % 12

    # =>else add mode is year
    elif mode == 'y':
        current['y'] += add

    # =>return changed current object
    return current

# =============================================


def PCAL_SubtractToJalaliDate(current, subtract=1, mode='d'):
    """
    current:{'y','m','d'}
    add:65
    mode:'d'|'m'|'y'
    """
    if Glob.DEBUG_MODE:
        print('subtract', current, subtract, mode)
    # =>if subtract mode is day
    if mode == 'd':
        # =>divide days to 28 (less than 1 month)
        daysdivide = int(subtract/28)
        if daysdivide < subtract/28:
            daysdivide += 1
        # =>iterate by daysdivide, and ‍every time just subtract 28 days or less!
        for i in range(0, daysdivide, 1):
            # =>calc tmp add, if bigger than 28, set 28, else tmpadd
            tmpadd = subtract-(i*28)
            if tmpadd > 28:
                tmpadd = 28
            # =>subtract to current day,tmpadd!
            current['d'] -= tmpadd  # FIXME:
            # =>check is bigger than 29,30,31 days
            if current['m']-1 > 0:
                maxdays = PCAL_ReturnDaysFromJalaliMonth(
                    current['m']-1, current['y'])
            else:
                maxdays = PCAL_ReturnDaysFromJalaliMonth(12, current['y']-1)
            if current['d'] < 1:
                # =>get different and subtract one to month
                diff = maxdays+current['d']
                current['m'] -= 1
                current['d'] = diff
                # print(diff, maxdays)
                # =>check is less than 1 month
                if current['m'] < 1:
                    # =>get different and subtract one from year
                    diff = current['m']+12
                    current['y'] -= 1
                    # =>calc year and month by diff
                    current['y'] -= int(diff/12)
                    current['m'] = diff % 12

    # =>else if subtract mode is month
    elif mode == 'm':
        current['m'] -= subtract
        # =>if was less than 1 month
        if current['m'] < 1:
            # =>get different and subtract one from year
            diff = current['m']+12
            current['y'] -= 1
            # =>calc year and month by diff
            current['y'] -= int(diff/12)
            current['m'] = diff % 12

    # =>else subtract mode is year
    elif mode == 'y':
        current['y'] -= subtract

    # =>return changed current object
    return current
# =============================================


def PCAL_ReturnDaysFromJalaliMonth(month, year):
    # =>count days for 6 first months
    if month < 7:
        return 31
    # =>count days for 5 secondary months
    elif month > 6 and month < 12:
        return 30
    # =>count days for last month
    elif month == 12:
        if PCAL_IsLeapYear(year):
            return 30
        return 29
# =============================================


def PCAL_CalculateHumanlyInterval(date, lang, sign):
    # =>init vars
    final = ''
    # =>check if year not zero
    if date['y'] > 0:
        final = '{} {}'.format(date['y'], lang['dictionary']['years'])
    # =>check if month not zero
    if date['m'] > 0:
        if final != '':
            final += ' {} '.format(lang['dictionary']['and'])
        final += '{} {}'.format(date['m'], lang['dictionary']['months'])
    # =>check if day not zero
    if date['d'] > 0:
        if final != '':
            final += ' {} '.format(lang['dictionary']['and'])
        final += '{} {}'.format(date['d'], lang['dictionary']['days'])
    # =>check sign of date as later or ago
    if sign:
        final += ' '+lang['dictionary']['later']
    else:
        final += ' '+lang['dictionary']['ago']
    # =>return final string
    return final

# =============================================
def PCAL_ReturnCorrectPath(relpath):
    return os.path.join(os.path.dirname(__file__),relpath)
# =============================================
def PCAL_ReturnEventsFromJalaliDay(year, month, day, returnjusttype=False):
    # =>init vars
    eventslist = []
    maintype = 'normal'  # 1)personal 2)holiday 3)occasion
    # =>get list of event files in events dir
    listfiles = os.listdir(PCAL_ReturnCorrectPath('events'))
    if Glob.DEBUG_MODE:
        print('list event files:', listfiles)
    # =>iterate event files, search for current date
    for evfile in listfiles:
        jsonc = ''
        # =>open and read all lines of json file
        with open(os.path.join(PCAL_ReturnCorrectPath('events'), evfile), 'r', encoding='utf8') as content_file:
            jsonc = content_file.read()
        # =>load json in events var
        events = json.loads(jsonc)
        # =>check metadata for startyear and endyear
        metadata = events['meta']
        if int(metadata['startyear']) > year or int(metadata['endyear']) <= year:
            continue
        # =>check for exist month and day
        if str(month) in events and str(day) in events[str(month)]:
            eventtext = events[str(month)][str(day)]
            eventtype = metadata['type']
            # =>if return just type is true
            if returnjusttype:
                if eventtype == 'personal':
                    maintype = eventtype
                elif eventtype == 'holiday' and maintype !='personal':
                    maintype = eventtype
                elif eventtype == 'occasion' and maintype == 'normal':
                    maintype = eventtype
            else:
                eventslist.append(
                    {'name': evfile, 'type': eventtype, 'author': metadata['author'], 'month': month, 'day': day, 'text': eventtext})

    # =>return events list,if returnjusttype is false(by default)
    if not returnjusttype:
        return eventslist
    else:
        return maintype
