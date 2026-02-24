from rest_framework import serializers
from .models import Event, Recurrence, EventOccurrence
from .tasks import generate_event_occurrences

class EventSerializer(serializers.ModelSerializer):
    recurrence = serializers.DictField(required=False, allow_null=True)

    class Meta:
        model = Event
        fields = ['id', 'title', 'description', 'start_date', 'end_date', 'recurrence']

    def to_representation(self, instance):
        data = super().to_representation(instance)
        rec = instance.recurrences.first()
        if rec:
            data['recurrence'] = {
                'frequency': rec.frequency,
                'end_date': rec.end_date.isoformat() if rec.end_date else None,
                'count': rec.count or 0,
            }
        else:
            data['recurrence'] = None
        return data

    def create(self, validated_data):
        recurrence = validated_data.pop('recurrence', None)
        event = Event.objects.create(**validated_data)
        if recurrence:
            Recurrence.objects.create(event=event, **recurrence)
        generate_event_occurrences.delay(event.id)  # Generate initial occurrences
        return event

    def update(self, instance, validated_data):
        recurrence = validated_data.pop('recurrence', None)
        instance.title = validated_data.get('title', instance.title)
        instance.description = validated_data.get('description', instance.description)
        instance.start_date = validated_data.get('start_date', instance.start_date)
        instance.end_date = validated_data.get('end_date', instance.end_date)
        instance.save()
        if recurrence is not None:
            instance.recurrences.all().delete()
            instance.occurrences.all().delete()
            if recurrence:
                Recurrence.objects.create(event=instance, **recurrence)
       
        generate_event_occurrences.delay(instance.id)
        return instance


class RecurrenceSerializer(serializers.ModelSerializer):
    event_name = serializers.SerializerMethodField()
    class Meta:
        model = Recurrence
        fields = ['id', 'frequency', 'end_date', 'count','event_name','event']
        
    def get_event_name(self, obj):
        return obj.event.title

    def update(self, instance, validated_data):
        instance.frequency = validated_data.get('frequency', instance.frequency)
        instance.end_date = validated_data.get('end_date', instance.end_date)
        instance.count = validated_data.get('count', instance.count)
        instance.save()
        generate_event_occurrences.delay(instance.event.id)
        return instance
        
        
class EventOccurrenceSerializer(serializers.ModelSerializer):
    event_name = serializers.SerializerMethodField()
    class Meta:
        model = EventOccurrence
        fields = ['id', 'event_name', 'start', 'end' ]
        
    def get_event_name(self, obj):
        return obj.event.title

    
    