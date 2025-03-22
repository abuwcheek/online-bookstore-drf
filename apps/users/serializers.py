from rest_framework import serializers
from django.contrib.auth import authenticate
from .models import CustomUser




class CustomUserRegisterSerializers(serializers.ModelSerializer):

     confirm_password = serializers.CharField(write_only=True)  # ✅ Modelga bog‘liq emas
     class Meta:
          model = CustomUser
          fields = ['username', 'email', 'first_name', 'last_name', 'avatar', 'phone', 'gender', 'birth_date', 'password', 'confirm_password']
          extra_kwargs = {
               'password': {'write_only': True},
               'confirm_password': {'write_only': True}
          }


     def validate(self, attrs):
          # parollarni solishtirish
          if attrs['password'] != attrs['confirm_password']:
               raise serializers.ValidationError({'password': 'parollar bir-biriga mos emas'})
          

          # username ni solishtirish
          if CustomUser.objects.filter(username=attrs['username']).exists():
               raise serializers.ValidationError({'username': "bu username oldin ro'yxatdan o'tgan"})
          

          # email ni solishtirish
          if CustomUser.objects.filter(email=attrs['email']).exists():
               raise serializers.ValidationError({'email': "bu email oldin ro'yxatdan o'tgan"})

          return attrs
     

     def create(self, validated_data):
          validated_data.pop("confirm_password")  # ✅ Bu field bazaga ketmasligi kerak
          user = CustomUser.objects.create_user(**validated_data)
          return user
     


class LogInUserSerializers(serializers.Serializer):
     username = serializers.CharField()
     password = serializers.CharField(write_only=True)


     def validate(self, attrs):
          username = attrs.get('username', None)
          password = attrs.get('password', None)
          
          user = authenticate(username=username, password=password)
          if not user:
               raise serializers.ValidationError({'login': 'login yoki parol xato'})
          
          attrs['user'] = user
          return attrs