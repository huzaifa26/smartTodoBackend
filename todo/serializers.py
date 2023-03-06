from rest_framework import serializers
from .models import Todo
from datetime import datetime


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
            # today = datetime.now().date()
            print(Todo.objects.filter(title=value, user=user, start_time__date=date).exists())
            if Todo.objects.filter(title=value, user=user, start_time__date=date).exists():
                raise serializers.ValidationError('You already have a Todo with this title.')
        return value

    def validate(self, data):
        start_time = data.get('start_time', None)
        end_time = data.get('end_time', None)
        if start_time and end_time and end_time <= start_time:
            raise serializers.ValidationError('End time must be after start time.')
        return data