

def time_zones(tz):

    supported_timezones = {
        'utc': 'UTC',
        'jst': 'Asia/Tokyo',
        'pt': 'America/Los_Angeles',
        'cst': 'America/Chicago',
        'ct': 'America/Chicago',
        'et': 'US/Eastern',
        'cet': 'Europe/Brussels',
        'aedt': 'Australia/Sydney',
        'sgt': 'Asia/Singapore',
        'in': 'Asia/Calcutta',
        'br': 'America/Sao_Paulo',
        'ca': 'America/Toronto',
        'kt': 'Asia/Seoul'
    }

    if tz in supported_timezones:
        return supported_timezones[tz]
    else:
        return supported_timezones['utc']
