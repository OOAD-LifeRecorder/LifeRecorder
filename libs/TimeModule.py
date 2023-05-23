from datetime import datetime, timedelta

def get_month_information(today: datetime = datetime.now()):
    next_month = today + timedelta(days=(30 if today.day > 10 else 20))
    first_day = today.replace(day=1)
    last_day = next_month.replace(day=1) - timedelta(days=1)
    
    return {
        'today': today,
        'first_day': first_day,
        'last_day': last_day
    }

def get_weekday_str(week_num: int):
    week = ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"]
    return week[week_num]