from rest_framework import serializers
from theApp.models.spam import Spam

class SpamSerializer(serializers.ModelSerializer):
    class Meta:
        model = Spam
        fields = '__all__'
