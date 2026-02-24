
from django.conf import settings
from django.db import models
from django.utils import timezone
import uuid


class SoftDeleteQuerySet(models.QuerySet):


    def with_deleted(self):
        return self.all()

    def delete(self, *args, **kwargs):
        from event_manager.current_user import get_current_user
        user = get_current_user()
        now = timezone.now()
        return self.update(
            is_deleted=True,
            deleted_at=now,
            deleted_by_id=user.pk if user else None,
        )


class SoftDeleteManager(models.Manager):
 

    def get_queryset(self):
        return SoftDeleteQuerySet(self.model, using=self._db).filter(is_deleted=False)

    def with_deleted(self):
        return SoftDeleteQuerySet(self.model, using=self._db)


class UUIDModel(models.Model):


    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False,
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_deleted = models.BooleanField(default=False)
    deleted_at = models.DateTimeField(null=True, blank=True)
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="%(class)s_created",
    )
    updated_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="%(class)s_updated",
    )
    deleted_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="%(class)s_deleted",
    )

    objects = SoftDeleteManager()

    class Meta:
        abstract = True

    def save(self, *args, **kwargs):
        from event_manager.current_user import get_current_user
        user = get_current_user()
        if user:
            if self._state.adding:
                self.created_by = user
            self.updated_by = user
        super().save(*args, **kwargs)

    def delete(self, soft=True, *args, **kwargs):
        from event_manager.current_user import get_current_user
        if soft and hasattr(self, "is_deleted"):
            user = get_current_user()
            if user:
                self.deleted_by = user
            self.deleted_at = timezone.now()
            self.is_deleted = True
            self.save(update_fields=["is_deleted", "deleted_at", "deleted_by", "updated_at"])
        else:
            super().delete(*args, **kwargs)
