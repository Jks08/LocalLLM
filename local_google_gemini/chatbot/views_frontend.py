from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from .API_KEY import *
import google.generativeai as genai
import textwrap

GOOGLE_API_KEY= api_key
genai.configure(api_key=GOOGLE_API_KEY)

def to_markdown(text):
    text = text.replace('•', '•')
    return textwrap.indent(text, '> ', predicate=lambda _: True)

class ChatSession:
    def __init__(self):
        self.model = genai.GenerativeModel('gemini-pro')
        self.chat = self.model.start_chat(history=[])

    def ask_question(self, question):
        # response = self.chat.send_message(question, safety_settings={'HARM_CATEGORY_HARASSMENT':'BLOCK_ONLY_HIGH', 'HARM_CATEGORY_SEXUALLY_EXPLICIT':'BLOCK_ONLY_HIGH', 'HARM_CATEGORY_HATE_SPEECH':'BLOCK_ONLY_HIGH','HARM_CATEGORY_DANGEROUS_CONTENT':'BLOCK_ONLY_HIGH'})
        response = self.chat.send_message(question)
        print(response.prompt_feedback)
        return response

chat_session = ChatSession()
chat_history = []

@csrf_exempt
def chat_page(request):
    global chat_history

    if request.method == 'POST':
        input_text = request.POST.get('input_text')

        if request.POST.get('clear_history'):
            chat_history = [] 
        else:
            try:
                response = chat_session.ask_question(input_text)
            except Exception as e:
                response = f"Input is invalid due to: \n{e}"

            chat_history.append({"role": "User", "text": input_text})
            try:
                chat_history.append({"role": "Gemini", "text": response.text})
            except:
                chat_history.append({"role": "Gemini", "text": response})

    return render(request, 'chatbot/chat_page.html', {'chat_history': chat_history})

def ClearHistory(request):
    global chat_history
    chat_history = []
    return render(request, 'chatbot/chat_page.html', {'chat_history': chat_history})