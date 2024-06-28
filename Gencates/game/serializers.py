from rest_framework import serializers
from .models import Cat, UserProfile, Incubator, Storage, Crossbreeder, IncomeRoom, HibernationRoom, CatyCoin


class CatSerializer(serializers.ModelSerializer):
    class Meta:
        model = Cat
        fields = '__all__'


class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        fields = ['user', 'coins', 'level', 'referral_code', 'referred_by', 'referrals_count']


class IncubatorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Incubator
        fields = '__all__'


class StorageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Storage
        fields = '__all__'


class CrossbreederSerializer(serializers.ModelSerializer):
    class Meta:
        model = Crossbreeder
        fields = '__all__'


class IncomeRoomSerializer(serializers.ModelSerializer):
    class Meta:
        model = IncomeRoom
        fields = '__all__'


class HibernationRoomSerializer(serializers.ModelSerializer):
    class Meta:
        model = HibernationRoom
        fields = '__all__'


class CatyCoinSerializer(serializers.ModelSerializer):
    class Meta:
        model = CatyCoin
        fields = '__all__'
