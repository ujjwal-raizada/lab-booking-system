import datetime
from .models import Slot, Instrument

lab_start_time = [datetime.time(hour=9), datetime.time(hour=14)]
lab_close_time = [datetime.time(hour=13), datetime.time(hour=17)]
INTERVAL_CHOICES = {
        "1-hour" : datetime.timedelta(hours=1),
        "2-hour" : datetime.timedelta(hours=2),
        "morning-session" : datetime.timedelta(hours=4),
        "evening-session" : datetime.timedelta(hours=3),
    }

def get_session_id(time):
    pass

def generate_slots(machine, interval, start=datetime.date.today(),
                   starttime=9, endtime=13, delta=7):
    machine = Instrument.objects.get(id=machine)
    gap = INTERVAL_CHOICES.get(interval)
    today_weekday = start.weekday()


    assert machine != None, Exception("Choose a valid machine id")
    assert interval in INTERVAL_CHOICES, Exception("Choose an authorised interval")
    assert get_session_id(starttime) == get_session_id(endtime), Exception("The lab has to be closed during lunch hours")

    next_days = [start + datetime.timedelta(days=var)
                for var in range(0, delta - today_weekday + 2)]
    all_slots = {}
    for day in next_days:
        day_wise = []
        for current, end in zip(lab_start_time, lab_close_time):
            while current < end:
                day_wise.append(datetime.datetime.combine(day, current))
                current = datetime.time(hour=(datetime.datetime.combine(day, current) + gap).hour)
        all_slots[day] = day_wise

    for day, time_slots in all_slots.items():
        try:
            for time_slot in time_slots:
                slot_obj = Slot(slot_name=machine.name, instrument=machine,
                                status=Slot.STATUS_1, date=day, time=time_slot.time())
                slot_obj.save()
        except:
            return False
    return True



if __name__ == "__main__":
    generate_slots(1, "1-hour", delta=2)
    print ("\n\n")
    generate_slots(None, "evening-session", starttime=14, endtime=17, delta=10)
