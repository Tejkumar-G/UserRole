"""
Models for Strategy to match flask app.
"""
from django.db import models


class Strategy(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    user_id = models.IntegerField()
    strategy_type = models.CharField(max_length=255, default='Public')
    class Meta:
        db_table = 'strategy'

    def __str__(self):
        return self.name
