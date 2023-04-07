from rest_framework import serializers
from .models import Todo
from datetime import datetime
from django.utils import timezone
from django.db.models import Q

class TodoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Todo
        fields = '__all__'
        read_only_fields = ('id', 'added_date', 'user')
        extra_kwargs = {
            'title': {'error_messages': {'required': 'Title field is required.'}},
            'description': {'error_messages': {'required': 'Description field is required.'}}
        }

    def validate_title(self, value):
        if self.instance is None:  # create request
            user = self.context['request'].data['user']
            date=self.context['request'].data['start_time']
            print(date)
            if date is not None:
                date=date.split()[0]
            if Todo.objects.filter(title=value, user=user, start_time__date=date).exists():
                raise serializers.ValidationError('You already have a Todo with this title.')
        return value
    
    def validate_start_time(self, value):
        if self.instance and self.context['request'].data['last_updated'] is not None:  # For updated tasks
            current_time=self.context['request'].data['last_updated']
            start_time=self.context['request'].data['start_time']
            date_format = '%Y-%m-%d %H:%M:%S'

            if start_time is not None:
                current_time = datetime.strptime(current_time, date_format)
                start_time = datetime.strptime(start_time, date_format)
                if start_time < current_time and self.context['request'].data['isStartTimeChange'] == False:
                    raise serializers.ValidationError('Start time must not be before the current time.')
            
        if self.instance is None:  # For new tasks
            current_time=self.context['request'].data['added_date']
            start_time=self.context['request'].data['start_time']
            end_time=self.context['request'].data['end_time']
            if start_time is not None:
                date_format = '%Y-%m-%d %H:%M:%S'
                current_time = datetime.strptime(current_time, date_format)
                start_time = datetime.strptime(start_time, date_format)
                if start_time < current_time:
                    raise serializers.ValidationError('Start time must not be before the current time.')
                
            if start_time is None and end_time is not None:
                date_format = '%Y-%m-%d %H:%M:%S'
                current_time = datetime.strptime(current_time, date_format)
                end_time = datetime.strptime(end_time, date_format)
                if end_time < current_time:
                    raise serializers.ValidationError('End time must not be before the current time.')
        return value

    # def validate(self, data):
    #     start_time = data.get('start_time', None)
    #     end_time = data.get('end_time', None)
    #     if start_time and end_time and end_time <= start_time:
    #         raise serializers.ValidationError('End time must be after start time.')
    #     if self.instance is None: # For updated tasks
    #         user = user = self.context['request'].data['user']

    #         if start_time and end_time and user:
    #             overlapping_todos = Todo.objects.filter(Q(start_time__lt=end_time, end_time__gt=start_time) | Q(start_time__exact=start_time, end_time__exact=end_time),user=user,).exclude(pk=self.instance.pk if self.instance else None)

    #             if overlapping_todos.exists():
    #                 raise serializers.ValidationError('Another Todo with overlapping time already exists.')
    #     return data
