# todos/models.py
from django.db import models
from django.contrib.auth import get_user_model


class Todo(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True, null=True)
    category = models.CharField(max_length=100)
    activity_type = models.TextField(blank=True, null=True)
    completed = models.BooleanField(default=False)
    started=models.BooleanField(default=False)
    isMissed=models.BooleanField(default=False)
    auto_complete=models.BooleanField(default=False)
    added_date = models.DateTimeField()
    last_updated = models.DateTimeField(blank=True, null=True)
    start_time = models.DateTimeField(blank=True, null=True)
    end_time = models.DateTimeField(blank=True, null=True)
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)

    def __str__(self):
        return self.title