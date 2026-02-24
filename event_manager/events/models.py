from django.db import models
from django.core.exceptions import ValidationError
from event_manager.base_models import UUIDModel


class Event(UUIDModel):
    """Event with optional description and optional recurrence."""

    title = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    start_date = models.DateTimeField()
    end_date = models.DateTimeField()

    class Meta:
        ordering = ['start_date']

    def __str__(self):
        return self.title


class Recurrence(UUIDModel):
    RECURRENCE_CHOICES = (
        ('daily', 'Daily'),
        ('weekly', 'Weekly'),
        ('monthly', 'Monthly'),
    )
    event = models.ForeignKey(Event, on_delete=models.CASCADE, related_name='recurrences')
    frequency = models.CharField(max_length=255, choices=RECURRENCE_CHOICES)
    end_date = models.DateTimeField(null=True, blank=True)
    count = models.IntegerField(default=0)
    class Meta:
        verbose_name_plural = 'Recurrences'

    def clean(self):
        if not self.end_date and not self.count:
            raise ValidationError('Either end_date or count must be set.')
        if self.end_date and self.count:
            raise ValidationError('Set either end_date or count, not both.')

    def save(self, *args, **kwargs):
        self.full_clean()
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.event.title} - {self.get_frequency_display()}"


class EventOccurrence(UUIDModel):
    """A single occurrence of an event (one-off or generated from recurrence)."""

    event = models.ForeignKey(
        Event,
        on_delete=models.CASCADE,
        related_name='occurrences',
    )
    recurrence = models.ForeignKey(
        Recurrence,
        on_delete=models.CASCADE,
        related_name='occurrences',
        null=True,
        blank=True,
    )
    start = models.DateTimeField()
    end = models.DateTimeField()

    class Meta:
        ordering = ['start']

    def __str__(self):
        return f"{self.event.title} @ {self.start}"

