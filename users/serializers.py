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
        fields = ('id', 'username', 'email', 'password')

class LoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField()

    def validate(self, attrs):
        user = authenticate(username=attrs['username'], password=attrs['password'])
        if not user:
            raise serializers.ValidationError("Invalid login credentials")
        attrs['user'] = user
        data={"id":user.id,"username":user.username,"email":user.email}
        return attrs,data