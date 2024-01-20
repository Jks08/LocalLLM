# chatbot/serializers.py
from rest_framework import serializers

class InputDataSerializer(serializers.Serializer):
    input_data = serializers.CharField()
