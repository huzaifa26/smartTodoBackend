# todos/models.py
from django.db import models
from django.contrib.auth.models import User

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
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.title