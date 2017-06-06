import datetime
import pytz
from utils.timezones import time_zones
from utils.CalculateHours import calc_hours


def validate_schedule(resource, this_tag, customTagName):

    t = this_tag

    if t['Key'].lower() == customTagName.lower():

        state = resource.state['Name']
        stop_instance = False
        start_instance = False

        all_schedules = []
        replace_white_space = t['Value'].replace(" ", "")
        replace_white_space = replace_white_space.lower()
        multiSchedule = replace_white_space.split('&')

        for grammar in multiSchedule:
            if grammar == '':
                continue
            ptag = grammar.split(";")

            if ptag[0].lower() in ['inactive', 'alternative']:
                continue

            if len(ptag) == 1 and ptag == ['followthesun']:
                ptag = ['1900', '1500', 'pt', 'followthesun']

            elif len(ptag) < 4 \
                or len(ptag[0]) != 4 \
                or len(ptag[1]) != 4 \
                or not ptag[0].isdigit() \
                or not ptag[1].isdigit():

                print("Invalid expression: '{}' must be of the form '%H%M;%H%M;timezone;<daysActive>' ".format(ptag))
                continue

            stopTime = ptag[0]
            startTime = ptag[1]
            timeZone = ptag[2].lower()
            daysActive = ptag[3].lower()

            isActiveDay = False
            isWeekend = False
            isGlobalWeekend = False
            isLogging = False

            tz = time_zones(timeZone)
            if tz == 'UTC':
                ptz = pytz.UTC
            else:
                ptz = pytz.timezone(tz)

            now = datetime.datetime.now(tz=ptz).strftime("%H%M")
            nowMax = datetime.datetime.now(tz=ptz) - datetime.timedelta(minutes=45)
            nowMax = nowMax.strftime("%H%M")
            nowDay = datetime.datetime.now(tz=ptz).strftime("%a").lower()


            # Days Interpreter
            if daysActive == "all":
                isActiveDay = True

            elif daysActive == "weekdays":
                weekdays = ['mon', 'tue', 'wed', 'thu', 'fri']
                if nowDay in weekdays:
                    isActiveDay = True

            elif daysActive == "weekends":
                weekends = ["fri", "sat", "sun", "mon"]
                if nowDay in weekends:
                    isActiveDay = True
                    isWeekend = True

            # 1900;1500;pst;followthesun
            elif daysActive == 'followthesun':
                global_weekend = ['fri', 'sat', 'sun']
                if nowDay in global_weekend:
                    isActiveDay = True
                    isGlobalWeekend = True

            else:
                daysActive = daysActive.split(",")
                for d in daysActive:
                    if d.lower() == nowDay:
                        isActiveDay = True

            if daysActive == 'followthesun':

                # Weekend Stop/Start taking into account all timezones across th globe
                if nowDay in ['fri'] and stopTime >= str(nowMax) and stopTime <= str(now) \
                        and isActiveDay and isGlobalWeekend and state == "running":
                    stop_instance = True
                    isLogging = True

                    print " Global Weekend STOP list", resource.id

                if nowDay in ['sun'] and startTime >= str(nowMax) and startTime <= str(now) \
                        and isActiveDay and isGlobalWeekend and state == "stopped":
                    start_instance = True
                    isLogging = False
                    print " Global Weekend START list", resource.id

            elif daysActive == 'weekends':

                # Basic Weekend Stop
                if nowDay in ['fri'] and stopTime >= str(nowMax) and stopTime <= str(now) \
                        and isActiveDay and isWeekend and state == "running":
                    stop_instance = True
                    isLogging = True

                    print " Weekend STOP list", resource.id

                # Basic Weekend Start

                if nowDay in ['mon'] and startTime >= str(nowMax) and startTime <= str(now) \
                        and isActiveDay and isWeekend and state == "stopped":
                    start_instance = True
                    isLogging = False
                    print " Weekend START list", resource.id

            else:
                # Append to stop list
                if stopTime >= str(nowMax) and stopTime <= str(now) and \
                        isActiveDay and state == "running":
                    stop_instance = True
                    isLogging = True

                    print " added to STOP list", resource.id

                # Append to start list
                if startTime >= str(nowMax) and startTime <= str(now) and \
                        isActiveDay and state == "stopped":
                    start_instance = True
                    isLogging = False

                    print " added to START list", resource.id

            # For logging the implicit weekend
            if daysActive == 'weekdays' and nowDay == 'fri':
                daysActive = 'weekends'

            totalhours = calc_hours(daysActive, stopTime, startTime)

            single_schedule = {
                'resource_id': resource.id,
                'start_instance': start_instance,
                'stop_instance': stop_instance,
                'stop_time': stopTime,
                'start_time': startTime,
                'tz': tz,
                'daysActive': daysActive,
                'grammar': grammar,
                'isLogging': isLogging,
                'TotalHours': totalhours
            }

            all_schedules.append(single_schedule)

        return all_schedules
