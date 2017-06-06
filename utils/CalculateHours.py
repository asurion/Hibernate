from __future__ import division


def calc_hours(schedule, stopTime, startTime):

    stop_mins = round(100 * (int(stopTime[2:])/60), -1)
    start_mins = round(100 * (int(startTime[2:]) / 60), -1)

    if stop_mins != 0:
        x = str(stopTime[:2])+str(int(stop_mins))
        stopTime = x

    if start_mins != 0:
        x = str(startTime[:2]) + str(int(startTime))
        startTime = x



    if schedule == 'followthesun':
        totalhours = 4600

    elif schedule == 'weekends':
        fri = 2400 - int(stopTime)
        mon = int(startTime)

        totalhours = 4800 + fri + mon

    elif schedule == 'weekdays' or schedule == 'all' or schedule in ['mon', 'tue', 'wed', 'thu', 'fri', 'sat', 'sun']:
        if stopTime < startTime:
            totalhours = int(startTime) - int(stopTime)
        else:
            totalhours = 2400 - abs(int(stopTime) - int(startTime))
    else:
        totalhours = 0

    th = totalhours/100
    return th

#print calc_hours('fri', '0100', '0200')

