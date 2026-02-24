from django.urls import path
from .views import EventListView, EventFormView, EventCalendarView, EventRegisterView

app_name = "events"

urlpatterns = [
    path("", EventListView.as_view(), name="list"),
    path("events/new/", EventFormView.as_view(), name="form"),
    path("events/calendar/", EventCalendarView.as_view(), name="calendar"),
    path("register/", EventRegisterView.as_view(), name="register"),
]
