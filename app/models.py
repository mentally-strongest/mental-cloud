# app/models.py
import os
import uuid

from django.conf import settings
from django.db import models
from django.template.defaultfilters import upper


class File(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='files')
    file = models.FileField(upload_to='uploads/')
    is_public = models.BooleanField(default=False)
    shared_link = models.UUIDField(default=uuid.uuid4, unique=True, editable=False, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    original_name = models.CharField(max_length=255)

    def save(self, *args, **kwargs):
        if not self.original_name:
            self.original_name = os.path.basename(self.file.name)
        super().save(*args, **kwargs)

    def delete(self, *args, **kwargs):
        if self.file:
            self.file.delete(save=False)
        super().delete(*args, **kwargs)

    def generate_shared_link(self):
        self.shared_link = uuid.uuid4()
        self.save()

    def delete_shared_link(self):
        self.shared_link = None
        self.save()

    def get_extension(self):
        return os.path.splitext(self.file.name)[1]

    def get_icon_name(self):
        return upper(self.get_extension()[1:])


    def get_size(self):
        return self.file.size

    def __str__(self):
        return f"{self.original_name} ({'Public' if self.is_public else 'Private'})"
