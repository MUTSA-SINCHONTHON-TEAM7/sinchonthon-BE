from rest_framework import serializers

from .models import MutsaUser

class MutsaUserResponseSerializer(serializers.ModelSerializer):
    class Meta:
        model = MutsaUser
        fields = ['id', 'nickname', 'kakao_sub']
        extra_kwargs = {
            field: {'read_only': True} for field in fields
        }

class KakaoLoginRequestSerializer(serializers.Serializer):
    access_code = serializers.CharField()
    
class MutsaUserPatchSerializer(serializers.Serializer):
    nickname = serializers.CharField()