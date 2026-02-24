from celery import shared_task
from .models import Event, Recurrence, EventOccurrence
from dateutil.rrule import rrule, DAILY, WEEKLY, MONTHLY

@shared_task
def generate_event_occurrences(event_id):
    event = Event.objects.get(id=event_id)
    recurrence = event.recurrences.first()
    if not recurrence:
        EventOccurrence.objects.create(event=event, start=event.start_date, end=event.end_date,created_by=event.created_by,updated_by=event.updated_by)
        return True

    freq_map = {
        "daily": DAILY,
        "weekly": WEEKLY,
        "monthly": MONTHLY,
    }
    freq = freq_map.get(recurrence.frequency, DAILY)
    duration = event.end_date - event.start_date

    if recurrence.end_date:
        rule = rrule(freq, dtstart=event.start_date, until=recurrence.end_date)
    else:
        rule = rrule(freq, dtstart=event.start_date, count=recurrence.count or 1)
    
    

    occurrences = [
        EventOccurrence(event=event, start=dt, end=dt + duration, recurrence=recurrence,created_by=event.created_by,updated_by=event.updated_by)
        for dt in rule
    ]
    if occurrences:
        EventOccurrence.objects.bulk_create(occurrences)
    return True

    
