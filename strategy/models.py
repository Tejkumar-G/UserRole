"""
Models for Strategy to match flask app.
"""
from datetime import datetime
from django.db import models


class Strategy(models.Model):
    name = models.CharField(max_length=255)
    description = models.CharField(max_length=255, blank=True, null=True)
    created_at = models.DateTimeField(default=datetime.utcnow, null=False)
    user_id = models.IntegerField()

    class Meta:
        db_table = 'strategy'

    def __str__(self):
        return self.name
