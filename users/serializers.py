from django.contrib.auth import get_user_model
from rest_framework import serializers
from django.contrib.auth import authenticate

class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    def create(self, validated_data):
        User=get_user_model()
        user = User.objects.create(
            username=validated_data['username'],
            email=validated_data['email'],
            # totalHours=0
        )
        user.set_password(validated_data['password'])   
        user.save()
        return user

    class Meta:
        model = get_user_model()
        fields = ('id', 'username', 'email', 'password','first_name','last_name')

class LoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField()

    def validate(self, attrs):
        user = authenticate(username=attrs['username'], password=attrs['password'])
        if not user:
            raise serializers.ValidationError("Invalid login credentials")
        attrs['user'] = user
        data={"id":user.id,"username":user.username,"email":user.email,'first_name':user.first_name,'last_name':user.last_name,}
        return attrs,data
    
class ChangePasswordSerializer(serializers.Serializer):
    old_password = serializers.CharField(required=True)
    new_password = serializers.CharField(required=True)

    def validate(self, data):
        User = get_user_model()
        user = User.objects.get(id=self.context['request'].data['id'])
        print(not user.check_password(data['old_password']))
        if not user.check_password(data['old_password']):
            raise serializers.ValidationError({'error': 'Wrong password.'})
        return data
