from django.shortcuts import render
from django.views.generic import TemplateView
from .models import Event, Recurrence, EventOccurrence
from .serializers import EventSerializer, RecurrenceSerializer, EventOccurrenceSerializer
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated

# Create your views here

class EventView(APIView):
    permission_classes = [IsAuthenticated]
    serializer_class = EventSerializer
    def get(self, request):
        events = Event.objects.filter(created_by=request.user)
        print(events)
        serializer = self.serializer_class(events, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    
    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class EventDetailView(APIView):
    permission_classes = [IsAuthenticated]
    serializer_class = EventSerializer
    def get(self, request, pk):
        try:
            event = Event.objects.get(id=pk, created_by=request.user)
            serializer = self.serializer_class(event)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Event.DoesNotExist:
            return Response({"detail": "Event not found"}, status=status.HTTP_404_NOT_FOUND)
        
    def put(self, request, pk):
        try:
            event = Event.objects.get(id=pk, created_by=request.user)
            serializer = self.serializer_class(event, data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_200_OK)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Event.DoesNotExist:
            return Response({"detail": "Event not found"}, status=status.HTTP_404_NOT_FOUND)

    def delete(self, request, pk):
        try:
            event = Event.objects.get(id=pk, created_by=request.user)
            event.occurrences.all().delete()    
            event.recurrences.all().delete()
            event.delete()
            return Response({"detail": "Event deleted"}, status=status.HTTP_200_OK)
        except Event.DoesNotExist:
            return Response({"detail": "Event not found"}, status=status.HTTP_404_NOT_FOUND)

class RecurrenceView(APIView):
    permission_classes = [IsAuthenticated]
    serializer_class = RecurrenceSerializer
    def get(self, request, pk):
        recurrence = Recurrence.objects.filter(event=pk, created_by=request.user)
        if not recurrence.exists():
            return Response({"detail": "Recurrence not found"}, status=status.HTTP_404_NOT_FOUND)
        recurrence = recurrence.first()
        serializer = self.serializer_class(recurrence)
        return Response(serializer.data, status=status.HTTP_200_OK)

class RecurrenceDetailView(APIView):
    permission_classes = [IsAuthenticated]
    serializer_class = RecurrenceSerializer
    def get(self, request, pk):
        try:
            recurrence = Recurrence.objects.get(id=pk, created_by=request.user)
            serializer = self.serializer_class(recurrence)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Recurrence.DoesNotExist:
            return Response({"detail": "Recurrence not found"}, status=status.HTTP_404_NOT_FOUND)
    
    def put(self, request, pk):
        try:
            recurrence = Recurrence.objects.get(id=pk, created_by=request.user)
            serializer = self.serializer_class(recurrence, data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_200_OK)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Recurrence.DoesNotExist:
            return Response({"detail": "Recurrence not found"}, status=status.HTTP_404_NOT_FOUND)
    
    def delete(self, request, pk):
        try:
            recurrence = Recurrence.objects.get(id=pk, created_by=request.user)
            recurrence.delete()
            return Response({"detail": "Recurrence deleted"}, status=status.HTTP_200_OK)
        except Recurrence.DoesNotExist:
            return Response({"detail": "Recurrence not found"}, status=status.HTTP_404_NOT_FOUND)


class EventOccurrenceView(APIView):
    permission_classes = [IsAuthenticated]
    serializer_class = EventOccurrenceSerializer
    def get(self, request):
        start_date = request.query_params.get('start_date')
        qs = EventOccurrence.objects.filter(created_by=request.user)
        if start_date:
            qs = qs.filter(start__gte=start_date)
        serializer = self.serializer_class(qs, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    

class EventOccurrenceDetailView(APIView):
    permission_classes = [IsAuthenticated]
    serializer_class = EventOccurrenceSerializer
    def get(self, request, pk):
        try:
            event_occurrence = EventOccurrence.objects.get(id=pk, created_by=request.user)
            serializer = self.serializer_class(event_occurrence)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except EventOccurrence.DoesNotExist:
            return Response({"detail": "Event occurrence not found"}, status=status.HTTP_404_NOT_FOUND)


# Frontend template views (no API logic)
class EventListView(TemplateView):
    template_name = "events/list.html"


class EventFormView(TemplateView):
    template_name = "events/form.html"


class EventCalendarView(TemplateView):
    template_name = "events/calendar.html"


class EventRegisterView(TemplateView):
    template_name = "events/register.html"

