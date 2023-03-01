from rest_framework import serializers
from .models import Todo


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
        user = self.context['request'].data['user']
        today = self.instance.added_date.date() if self.instance else self.context['request'].data.get('added_date', None)
        if Todo.objects.filter(title=value, user=user, added_date__date=today).exists():
            raise serializers.ValidationError('You already have a Todo with this title.')
        return value

    def validate(self, data):
        start_time = data.get('start_time', None)
        end_time = data.get('end_time', None)
        if start_time and end_time and end_time <= start_time:
            raise serializers.ValidationError('End time must be after start time.')
        return data