from django.urls import path
from .views import EventView, EventDetailView, RecurrenceView, RecurrenceDetailView, EventOccurrenceView, EventOccurrenceDetailView

urlpatterns = [
    path('events/', EventView.as_view(), name='events'),
    path('events/<uuid:pk>/', EventDetailView.as_view(), name='event-detail'),
    path('recurrences/', RecurrenceView.as_view(), name='recurrences'),
    path('recurrences/<uuid:pk>/', RecurrenceDetailView.as_view(), name='recurrence-detail'),
    path('event-occurrences/', EventOccurrenceView.as_view(), name='event-occurrences'),
    path('event-occurrences/<uuid:pk>/', EventOccurrenceDetailView.as_view(), name='event-occurrence-detail'),
]