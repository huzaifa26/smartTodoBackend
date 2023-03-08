from rest_framework import serializers
from .models import Todo
from datetime import datetime
from django.utils import timezone

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
            date=date.split()[0]
            if Todo.objects.filter(title=value, user=user, start_time__date=date).exists():
                raise serializers.ValidationError('You already have a Todo with this title.')
        return value
    
    # def validate_start_time(self, value):
        print(self.instance)
        if self.instance and self.context['request'].data['last_updated'] is not None: # For new tasks
            current_time=self.context['request'].data['last_updated']
            start_time=self.context['request'].data['start_time']
            date_format = '%Y-%m-%d %H:%M:%S'

            current_time = datetime.strptime(current_time, date_format)
            start_time = datetime.strptime(start_time, date_format)

            if start_time < current_time:
                raise serializers.ValidationError('Start time must not be before the current time.')
            
        if self.instance is None: # For updated tasks
            print(self.context['request'].data)
            current_time=self.context['request'].data['added_date']
            start_time=self.context['request'].data['start_time']
            date_format = '%Y-%m-%d %H:%M:%S'

            current_time = datetime.strptime(current_time, date_format)
            start_time = datetime.strptime(start_time, date_format)

            print(current_time)
            print(start_time)

            if start_time < current_time:
                raise serializers.ValidationError('Start time must not be before the current time.')

        return value

    def validate(self, data):
        start_time = data.get('start_time', None)
        end_time = data.get('end_time', None)
        if start_time and end_time and end_time <= start_time:
            raise serializers.ValidationError('End time must be after start time.')
        return data