from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .serializers import InputDataSerializer
from .API_KEY import *
import google.generativeai as genai

GOOGLE_API_KEY= api_key
genai.configure(api_key=GOOGLE_API_KEY)

class Single_InputDataProcessing:
    def __init__(self, user_input):
        self.user_input = user_input
    
    def model_to_use(self):
        model = genai.GenerativeModel('gemini-pro')
        return model

    def get_response(self):
        # model = genai.GenerativeModel('gemini-pro')
        model = self.model_to_use()
        output = model.generate_content(self.user_input)
        return output
    
class Chat_InputDataProcessing:
    def __init__(self, user_input):
        self.user_input = user_input
    
    def model_to_use(self):
        model = genai.GenerativeModel('gemini-pro')
        chat = model.start_chat(history=[])
        return chat

    def get_response(self):
        # model = genai.GenerativeModel('gemini-pro')
        model = genai.GenerativeModel('gemini-pro')
        chat = model.start_chat(history=[])
        output = chat.send_message(self.user_input)
        return output

class LandingPage(APIView):
    def get(self, request):
        # Use the landing_page.html template
        return render(request, 'landing_page.html')

class SingleInputDataView(APIView):
    def get(self, request):
        modelList = []

        for m in genai.list_models():
            if 'generateContent' in m.supported_generation_methods:
                modelList.append(m.name)
        
        return Response(modelList)
    
    def post(self, request, *args, **kwargs):
        serializer = InputDataSerializer(data=request.data)

        if serializer.is_valid():
            # Process the input data (serializer.validated_data['input_data'])
            input_data = serializer.validated_data['input_data']
            # Customize your processing logic here
            chatbot = Single_InputDataProcessing(input_data)
            output = chatbot.get_response()
            print(output.text)

            return Response({output.text}, status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
class ChatInputDataView(APIView):
    def get(self, request):
        modelList = []

        for m in genai.list_models():
            if 'generateContent' in m.supported_generation_methods:
                modelList.append(m.name)
        
        return Response(modelList)
    
    def post(self, request, *args, **kwargs):
        serializer = InputDataSerializer(data=request.data)

        if serializer.is_valid():
            # Process the input data (serializer.validated_data['input_data'])
            input_data = serializer.validated_data['input_data']
            # Customize your processing logic here
            chatbot = Chat_InputDataProcessing(input_data)  
            output = chatbot.get_response()
            print(output.text)

            return Response({output.text}, status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
